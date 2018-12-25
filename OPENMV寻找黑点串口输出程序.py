# Ѱ�Һڵ㴮��������� - By: Kevincoooool - ���� 11�� 23 2017
import sensor,time,pyb,math
from pyb import Pin, Timer, LED, UART
#��ɫ����ֵ
black_threshold = [(0, 64)]
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
while(True):
    clock.tick()
    img = sensor.snapshot()
    #Ѱ��blob
    blobs = img.find_blobs(black_threshold)
    if blobs:
        most_pixels = 0
        largest_blob = 0
        for i in range(len(blobs)):
            #Ŀ�������ҵ�����ɫ����ܲ�ֹһ**�ص�����**�����ҵ�����һ��
            if blobs[i].pixels() > most_pixels:
                most_pixels = blobs[i].pixels()
                largest_blob = i
                #λ�û��õ��ı���
                err_x = int(60 - blobs[largest_blob].cy())
                err_y = int(blobs[largest_blob].cx() - 80)
        img.draw_cross(blobs[largest_blob].cx(),blobs[largest_blob].cy())#����ʹ��
        img.draw_rectangle(blobs[largest_blob].rect())
    else:
       err_x = 0
       err_y = 0
    #����������д��
    uart_buf = bytearray([0x55,err_x>>8,err_x,err_y>>8,err_y,0xAA])
    print(err_x,err_y)
    uart.write(uart_buf)
