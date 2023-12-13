import serial
import socket
import os
import time
import schedule
import datetime
import csv
from serial.serialutil import SerialException
import shutil
import tempfile

def remove_null_lines(input_file_path):
    temp_file_path = tempfile.NamedTemporaryFile(mode='w', delete=False).name
    with open(input_file_path, 'r') as input_file, open(temp_file_path, 'w', newline='') as temp_file:
        reader = csv.reader(input_file)
        writer = csv.writer(temp_file)
        for row in reader:
            if any(field.strip() for field in row):
                writer.writerow(row)
    shutil.move(temp_file_path, input_file_path)


def get_last_timestamp(last_timestamp, serial_port):
    # Read CSV file, filter data based on last sent timestamp,
    # add device name to each row, and convert to JSON
    remove_null_lines("/home/morsestudio/Documents/new-lora-setup-code-main/gas_data.csv")
    with open("/home/morsestudio/Documents/new-lora-setup-code-main/gas_data.csv",'r') as csv_file:
        if csv_file: 
            print("Read Correctly")
    
        csv_reader = csv.DictReader(csv_file)
        #print(csv_reader)
        data = [
            {
                "timestamp": datetime.datetime.strptime(str(row["timestamp"]).strip(), "%m/%d/%y %H:%M:%S").strftime("%m/%d/%y %H:%M:%S"),
                "data_type": float(row["data_type"]),
                "data_point": str(row["data_point"])
            }
            for row in csv_reader
        ]
    if len(data) == 0:
        return last_timestamp
    else:
        for row in data:
            string_send = f"{row['timestamp'], row['data_type'], row['data_point']}"
            byte_str = bytes(string_send, 'utf-8')
            try:
                serial_port.write(byte_str)
                print("line written: "+ string_send)
            except SerialException as e:
                print("An Exeception occured with serial transmission", e)
            with open("/home/morsestudio/Documents/new-lora-setup-code-main/last_sent_timestamp.txt",'w') as file:
                file.write(f"{row['timestamp']}")
            time.sleep(10)
        
    # Return the last timestamp from the filtered CSV data
    last_row = data[-1] if data else None
    last_timestamp = last_row["timestamp"] if last_row else last_timestamp
    return last_timestamp
# Define function to schedule sending task every 30 minutes at regular times of the day
def schedule_get_last_timestamp(ser_port):
    # Initialize last sent timestamp to the earliest possible timestamp
    #last_timestamp = datetime.datetime.combine(datetime.date.today(),datetime.datetime.min.time()).strftime("%a %b  %d %H:%M:%S %Y")
    last_timestamp = ""
    with open("/home/morsestudio/Documents/new-lora-setup-code-main/last_sent_timestamp.txt",'r') as csv_file:
        last_timestamp = csv_file.read()
        # if datetime.datetime.strptime(str(last_line["timestamp"]).strip(), "%a %b  %d %H:%M:%S %Y") > datetime.datetime.strptime(last_timestamp, '%a %b  %d %H:%M:%S %Y')
        
    print(last_timestamp)
    print(' in scheduling')
    while True:
        now = datetime.datetime.now()
        if now.minute == 0 or now.minute == 30 or now.minute == 4:
            # Define the times of the day when the CSV da                                                              ta should be sent
            # send_times = [datetime.time(hour=h, minute=0) for h in range(0, 24)] + \
            #              [datetime.time(hour=h, minute=30) for h in range(0, 24)] + \
            #              [datetime.time(hour=h, minute=10) for h in range(0, 24)]
            # print('here')
            # print(send_times)
            # print(now.time())
            # Check if the current time is one of the send times
            print('inner loop')
            # Send CSV data and update last sent timestamp
            while True:
                last_timestamp = get_last_timestamp(last_timestamp, ser_port)
                break
                

        time.sleep(10)

# Run scheduling task indefinitely
def main():
    while True:
        try:
            ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
            print("success")
        except serial.serialutil.SerialException:
            print("UnSuccessful Connection to Serial Port")
        print('in main')
        schedule_get_last_timestamp(ser)

if __name__ == "__main__":
    main()
