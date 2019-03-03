import serial
import time
import datetime
import csv

from pathlib import Path

def isanumber(a):
    try:
        float(a)
        bool_a = True
    except:
        bool_a = False

    return bool_a

# TODO: figure out if we can search for arduino from all ports
# Arduino settings
test_name = input("Test Name: ")
csv_path = Path("./" + test_name + ".csv")
isStationary = (input("Stationary? (y/n)").lower()) == "y"

lat = None
lng = None

if (isStationary == True):
    lat = float(input("Lat: "))
    lng = float(input("Lng: "))

port = input("Port (COMXX or other format): ")
baudrate = 9600
connection_timeout = 5

# Setup serial connection -- will restart Arduino script
ard = serial.Serial(port, baudrate, timeout=connection_timeout)

with csv_path.open(mode="w") as f:
    writer = csv.writer(f)
    # write header
    writer.writerow(["Time", "Latitude", "Longitude", "RSSI", "Message"])

    i = 0

    # collect data
    last_rec_msg = ""
    while True:
        line = ard.readline()
        recieved_data = line[:-2]

        if (recieved_data):
            #print(recieved_data)
            recieved_data = str(recieved_data, 'utf-8')
            print(recieved_data, i)
            i += 1
            if "REC:" in recieved_data:
                last_rec_msg = recieved_data[4:]
            elif isanumber(recieved_data):
                rssi = int(recieved_data)
                time = datetime.datetime.now()
                print(rssi)
                if (isStationary == False):
                    lat = "NR"
                    lng = "NR"
                writer.writerow([time, lat, lng, rssi, last_rec_msg])
