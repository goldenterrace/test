# 寻找黑点串口输出程序 - By: Kevincoooool - 周四 11月 23 2017
import sensor,time,pyb,math
from pyb import Pin, Timer, LED, UART
#黑色点阈值
target_threshold = [(18, 34, 27, 62, -3, 55)]
#xy平面误差数据
err_x = 0
err_y = 0
#发送数据
uart_buf = bytearray([0x55,0xAA,0x00,0x00,0x00,0x00,0xAA])

#串口三配置
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置灰度信息
sensor.set_framesize(sensor.QQVGA)#设置图像大小
sensor.skip_frames(20)#相机自检几张图片
sensor.set_auto_whitebal(False)#关闭白平衡
clock = time.clock()#打开时钟

def order(blob):
    return blob.pixels()

while(True):
    clock.tick()
    img = sensor.snapshot()
    #寻找blob
    blobs = img.find_blobs(target_threshold, pixels_threshold=100, area_threshold=100)
    blobs.sort(key=order)
    if len(blobs) >= 2:
        b1 = blobs[-1]
        b2 = blobs[-2]
        center_x = img.width() // 2
        center_y = img.height() // 2
        x = (b2.cx() + b1.cx()) // 2
        y = (b1.cy() + b2.cy()) // 2
        img.draw_rectangle(b1.rect())
        #img.draw_cross(b1.cx(), b1.cy())
        img.draw_rectangle(b2.rect())
        img.draw_cross(center_x, center_y, color = (255,0,0))
        img.draw_cross(x, y, color=(0,255,0))
        err_x = center_x - x
        err_y = center_y - y
        img.draw_string(0,0, "diff: %d %d"%(err_x, err_y))
        #img.draw_string(0,0, str(blobs[0].w()*blobs[0].h()))
        #for i in range(len(blobs)):
            ##目标区域找到的颜色块可能不止一**重点内容**个，找到最大的一个
            #if blobs[i].pixels() > most_pixels:
                #most_pixels = blobs[i].pixels()
                #largest_blob = i
                ##位置环用到的变量
                #err_x = int(60 - blobs[largest_blob].cy())
                #err_y = int(blobs[largest_blob].cx() - 80)
        #img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())#调试使用
        #img.draw_rectangle(blobs[largest_blob].rect())
    else:
       img.draw_string(0,0, "not found!")
       err_x = 0
       err_y = 0
    #数组中数据写入
    uart_buf = bytearray([0x55,err_x>>8,err_x,err_y>>8,err_y,0xAA])
    print(err_x,err_y)
    uart.write(uart_buf)
