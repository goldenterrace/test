# 寻找黑点串口输出程序 - By: Kevincoooool - 周四 11月 23 2017
import sensor,time,pyb,math
from pyb import Pin, Timer, LED, UART
#黑色点阈值
threshold = [(11, 25, -41, -19, -9, 41)]
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

"""几种思路方法:
1. 排序再获取两个
2. 获取第一大，再获取第二大
3. 获取矩形，再根据statistics获取颜色范围，三重循环
4. 把两个当作整体获取（ncc，color code）
"""

while(True):
    clock.tick()
    img = sensor.snapshot()
    #寻找blob
    """todo: find_rects then
    area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())#area为识别到的圆的区域，即圆的外接矩形框
    statistics = img.get_statistics(roi=area)#像素颜色统计
    """

    blobs = img.find_blobs(threshold, pixels_threshold=200, area_threshold=200)
    """注意pixels和area阈值"""
    center = img.width()//2, img.height()//2
    img.draw_cross(center[0], center[1], color=(255,0,0))
    img.draw_string(center[0], center[1], "x:%s, y:%s"%(center[0], center[1]))

    if blobs and len(blobs)>=2:
        blobs.sort(key=order)
        blob1 = blobs[-1]
        blob2 = blobs[-2]
        #most_pixels = 0
        #largest_blob = 0
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

        x = (blob1.cx() + blob2.cx()) // 2
        y = (blob1.cy() + blob2.cy()) // 2
        err_x = int(center[0] - y)
        err_y = int(x - center[1])

        img.draw_rectangle(blob1.rect())
        img.draw_rectangle(blob2.rect())

        img.draw_cross(x, y, color=(0,255,0))#调试使用
        img.draw_string(x, y, "x:%s, y:%s"%(x, y))
        #img.draw_rectangle(blobs[largest_blob].rect())
    else:
       err_x = 0
       err_y = 0
    #数组中数据写入
    uart_buf = bytearray([0x55,err_x>>8,err_x,err_y>>8,err_y,0xAA])
    print(err_x,err_y)
    uart.write(uart_buf)
    uart.write("%d %d"%(err_x, err_y))
