import serial
import time
import datetime
import csv

from pathlib import Path

# TODO: figure out if we can search for arduino from all ports
# Arduino settings
test_name = input("Test Name: ")
csv_path = Path("./" + test_name + ".csv")
isStationary = (input("Stationary? (y/n)").lower()) == "y"

lat = None
lng = None

if (isStationary == True):
    lat = int(input("Lat: "))
    lng = int(input("Lng: "))

port = input("Port (COMXX or other format): ")
baudrate = 9600
connection_timeout = 5

# Setup serial connection -- will restart Arduino script
ard = serial.Serial(port, baudrate, timeout=connection_timeout)

with csv_path.open(mode="w") as f:
    writer = csv.writer(f)
    # write header
    writer.writerows(["Time", "Latitude", "Longitude", "RSSI"])

    # collect data
    while True:
        line = ard.readline()
        recieved_data = line[:-2]

        if (recived_data):
            if "REC:" in recieved_data:
                rec_msg = recieved_data[4:]
            else:
                rssi = int(recieved_data)
                time = datetime.datetime.now()
                if (isStationary == False):
                    lat = "NR"
                    lng = "NR"
                writer.writerows([time, lat, lng, rssi])
