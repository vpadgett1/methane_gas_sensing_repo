import serial
import socket
import os
import time
from datetime import datetime 
ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=.1)
#time.sleep(2)
previous = ''
while True:
    try:
        while ser.in_waiting:
            recv_from_cube = ser.readline()
            string_data = str(recv_from_cube)
            print("Incoming Data:" + string_data)
            with open('//home/morsestudio/Documents/new-lora-setup-code-main/gas_data.csv', 'a') as file:
                string_clean = string_data.split('b\'', 1)[1]
                string_clean = string_clean.split('\\n',1)[0]
                string_clean = string_clean.split('\\r',1)[0]
                split_data = string_clean.split(' ', 1)
                #print(split_data)
                data_type = split_data[0]
                data_point = split_data[1]
                #print(string_clean)
                if previous==string_clean or string_clean.isspace():
                    continue
                timestamp_for_data = datetime.now()
                timestamp_data = timestamp_for_data.strftime("%m/%d/%y %H:%M:%S")
                final_string = timestamp_data + "," + data_type + "," + data_point
                print(final_string)
                file.write(final_string)
                file.write('\n')
                previous=string_clean
                #print(string_clean)
    except ValueError:
        print('There were not enough values in the received string saving details of the string')
        with open('/home/demopi/Documents/gas_data.csv','a+') as file:
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            file.write(string_clean+', '+dt_string)
            file.write('\n')
