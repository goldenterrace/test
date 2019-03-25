# Ѱ�Һڵ㴮��������� - By: Kevincoooool - ���� 11�� 23 2017
import sensor,time,pyb,math
from pyb import Pin, Timer, LED, UART
#��ɫ����ֵ
target_threshold = [(18, 34, 27, 62, -3, 55)]
#xyƽ���������
err_x = 0
err_y = 0
#��������
uart_buf = bytearray([0x55,0xAA,0x00,0x00,0x00,0x00,0xAA])

#����������
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)#���ûҶ���Ϣ
sensor.set_framesize(sensor.QQVGA)#����ͼ���С
sensor.skip_frames(20)#����Լ켸��ͼƬ
sensor.set_auto_whitebal(False)#�رհ�ƽ��
clock = time.clock()#��ʱ��

def order(blob):
    return blob.pixels()

while(True):
    clock.tick()
    img = sensor.snapshot()
    #Ѱ��blob
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
            ##Ŀ�������ҵ�����ɫ����ܲ�ֹһ**�ص�����**�����ҵ�����һ��
            #if blobs[i].pixels() > most_pixels:
                #most_pixels = blobs[i].pixels()
                #largest_blob = i
                ##λ�û��õ��ı���
                #err_x = int(60 - blobs[largest_blob].cy())
                #err_y = int(blobs[largest_blob].cx() - 80)
        #img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())#����ʹ��
        #img.draw_rectangle(blobs[largest_blob].rect())
    else:
       img.draw_string(0,0, "not found!")
       err_x = 0
       err_y = 0
    #����������д��
    uart_buf = bytearray([0x55,err_x>>8,err_x,err_y>>8,err_y,0xAA])
    print(err_x,err_y)
    uart.write(uart_buf)
