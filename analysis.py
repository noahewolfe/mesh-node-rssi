# -*- coding: utf-8 -*-

import csv
from pathlib import Path
import pytz
from datetime import datetime, timedelta

import scipy.interpolate
import numpy as np
import pylab as pl

from mpl_toolkits.basemap import Basemap

def coord_distance(lat1, lon1, lat2, lon2):
    R = 6373.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance * 1000

# going to make the assumption we aren't at a very curvy part of the Earth
def max_offset(clat, clng, d):
    # find max lat offset
    max_lat_off = 0.001
    while( coord_distance(clat, clng, clat + max_lat_off, clng) > d ):
        max_lat_off -= 0.0000000001 # tiny change
                        
    # find max lng offset
    max_lng_off = 0.001
    while( coord_distance(clat, clng, clat, clng + max_lng_off) > d ):
        max_lng_off -= 0.0000000001 # tiny change

    return max_lat_off, max_lng_off

    """
    points = np.zeros((n,2))
    for idx,p in enumerate(range(0, n)):    
        angle = (2 * np.pi / n) * p
        points[idx,0] = clat + np.cos(angle) * max_lat_off
        points[idx,1] = clng + np.sin(angle) * max_lng_off
    
    return points[:,0], points[:,1] 
    """
    
track_path = Path(r"C:\Users\noahw\Google Drive\projects\air-pollution\rssi-testing\031919_1\track_points.csv")
node_path  = Path(r"C:\Users\noahw\Google Drive\projects\air-pollution\rssi-testing\031919_1\031919_1.csv")

est = pytz.timezone("US/Eastern")
utc = pytz.utc

#t_fmt = "%Y-%m-%d %H:%M:%S"

### Load Track Data ###
timed_coords = [] # [t, lat, lng]
with open(track_path, "r") as track_file:
    track_reader = csv.DictReader(track_file)
    for row in track_reader:
        # cut out +00 at the end, as it is troublesome... just remember, it is originally UTC!
        t_utc = datetime.strptime(row["time"][:-3], "%Y/%m/%d %H:%M:%S").replace(tzinfo=utc)
        t = t_utc.astimezone(est).replace(tzinfo=None)        
        lng = float(row["X"])
        lat = float(row["Y"])
        
        timed_coords.append([t, lat, lng])
    
### Load Stationary Node Data ###
node_timed_data = [] # [t, rssi] --> this is for a stationary node!
lat_stationary = None
lng_stationary = None
with open(node_path, "r") as node_file:
    node_reader = csv.DictReader(node_file)
    
    for row in node_reader:
        t = datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S.%f")#.replace(tzinfo=est)
        #t = t.astimezone(utc)
        rssi = float(row["RSSI"])
        node_timed_data.append([t, rssi])
        
        if lat_stationary is None and lng_stationary is None:
            lat_stationary = float(row["Latitude"])
            lng_stationary = float(row["Longitude"])
            
### Combine Data ###
t_tolerance = 1.5 # [s]

combined_t    = []
combined_lat  = []
combined_lng  = []
combined_rssi = []
for d in node_timed_data:   
    for c in timed_coords:
        datetime_diff = c[0] - d[0]
        diff = np.abs(datetime_diff.seconds) # diff in seconds
        if diff <= t_tolerance:
            combined_t.append(d[0])
            combined_lat.append(c[1])
            combined_lng.append(c[2])
            combined_rssi.append(d[1])

#y = np.random.uniform(35.6, 35.8, 100)
x = np.array(combined_lng, dtype=np.float64)
#x = np.random.uniform(-78.7,-78.5,100)
y = np.array(combined_lat, dtype=np.float64)
#z = np.random.uniform(-130,-90,100)
z = np.array(combined_rssi, dtype=np.float64)
# need to shape z!

### maybe change interpolation to be splines on the paramteric functions x(t), y(t).... where z = f(x,y)?
### need to review paramterization stuff

fig, ax = pl.subplots(1,1)

m = Basemap(
    resolution = None, 
    llcrnrlat = y.min(),
    llcrnrlon = x.min(),
    urcrnrlat = y.max(),
    urcrnrlon = x.max(),
    ax = ax
)

m.arcgisimage(service="World_Street_Map", xpixels = 1000, verbose= True, zorder=0)

stp = complex(len(x),1) # the complex makes mgrid inclusive on both bounds
xi, yi = np.mgrid[min(x):max(x):stp, min(y):max(y):stp]
Z = scipy.interpolate.griddata((x, y), z, (xi, yi), method="linear")

xi, yi = m(xi,yi)

m.contour(xi,yi,Z, latlon=True, cmap="viridis")
#m.colorbar()
m.scatter(x,y,c=z,edgecolors="gray",latlon=True, cmap="viridis")

### draw a 100m radius circle
#circ_x, circ_y = m(lng_stationary, lat_stationary)
#m. scatter(circ_x, circ_y, marker = "o", color="black", latlon=True)
#lat_off, lng_off = max_offset(lat_stationary, lng_stationary, 100)
#circ_x2, circy_2 = m(lng_stationary, lat_stationary + lat_off)
#circ = pl.Circle((circ_x, circ_y), circy_2 - circ_y, color="black", fill=False, zorder=100)
#ax.add_patch(circ)

#pl.show()