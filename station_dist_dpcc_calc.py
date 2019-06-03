# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 03:20:30 2019

@author: noahw
"""

import numpy as np

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

stations_from_dpcc = [
   ['Anand Vihar', 28.645892, 77.314853, 'AallStationView5MinData.php?stName=QW5hbmRWaWhhcg==', '../images/tree-active.png','Anand Vihar'],
	['Mandir Marg', 28.630362, 77.197293, 'AallStationView5MinData.php?stName=TWFuZGlybWFyZw==', '../images/tree-active.png','Mandir Marg'],
	['Punjabi Bagh', 28.661975, 77.124156, 'AallStationView5MinData.php?stName=UHVuamFiaUJhZ2g=', '../images/tree-active.png','Punjabi Bagh'],
	['R.K. Puram', 28.566008, 77.176743, 'AallStationView5MinData.php?stName=UktQdXJhbQ==', '../images/tree-active.png','R.K. Puram'],
	['IGI Airport', 28.556162, 77.099958, 'IGIAallStationView5MinData.php?stName=SUdJ', '../images/tree-active.png','IGI Airport'],
	['Civil Lines', 28.681428, 77.222687, 'IGIAallStationView5MinData.php?stName=Q2l2aWxsaW5lcw==', '../images/tree-active.png','Civil Lines'],
	['Dr. Karni Singh Shooting Range', 28.499727, 77.267095, 'AallStationView5MinData.php?stName=S2FybmlTaW5naFNob290aW5nUmFuZ2U=', '../images/tree-active.png','Dr. Karni Singh Shooting Range'],
	['Major Dhyan Chand National Stadium', 28.612498, 77.237388, 'AallStationView5MinData.php?stName=TmF0aW9uYWxTdGFkaXVt', '../images/tree-active.png','Major Dhyan Chand National Stadium'],
	['Nehru Nagar', 28.566827, 77.251418, 'AallStationView5MinData.php?stName=TmVocnVOYWdhcg==', '../images/tree-active.png','Nehru Nagar'],
	['Jahangirpuri', 28.733016, 77.171970, 'AallStationView5MinData.php?stName=SmFoYW5naXJwdXJp', '../images/tree-active.png','Jahangirpuri'],
	['Wazirpur', 28.700505, 77.165603, 'AallStationView5MinData.php?stName=V2F6aXJwdXI=', '../images/tree-active.png','Wazirpur'],
	['Patparganj', 28.620171, 77.287705, 'AallStationView5MinData.php?stName=UGF0cGFyZ2Fuag==', '../images/tree-active.png','Patparganj'],
	['Ashok Vihar', 28.695720, 77.181295, 'AallStationView5MinData.php?stName=QXNob2tWaWhhcg==', '../images/tree-active.png','Ashok Vihar'],
	['Okhla Phase-2', 28.531314, 77.270686, 'AallStationView5MinData.php?stName=T2tobGFQaGFzZTI=', '../images/tree-active.png','Okhla Phase-2'],
	['Rohini', 28.732743, 77.118788, 'AallStationView5MinData.php?stName=Um9oaW5pU2VjdG9yMTY=', '../images/tree-active.png','Rohini'],
	['Vivek Vihar', 28.672114, 77.313832, 'AallStationView5MinData.php?stName=Vml2ZWtWaWhhcg==', '../images/tree-active.png','Vivek Vihar'],
	['Sonia Vihar', 28.710066, 77.246220, 'AallStationView5MinData.php?stName=U29uaWFWaWhhcg==', '../images/tree-active.png','Sonia Vihar'],
	['Dwarka, Sector 8', 28.576909, 77.075898, 'AallStationView5MinData.php?stName=RHdhcmthU2VjdHJvOA==', '../images/tree-active.png','Dwarka, Sector 8'],
	['Najafgarh', 28.572714, 76.933433, 'AallStationView5MinData.php?stName=TmFqYWZnYXJo', '../images/tree-active.png','Najafgarh'],
	['Narela', 28.820629, 77.101099, 'AallStationView5MinData.php?stName=TmFyZWxh', '../images/tree-active.png','Narela'],
	['Pooth Khurd, Bawana', 28.7757959,77.0462514, 'AallStationView5MinData.php?stName=UG9vdGhLaHVyZEJhd2FuYQ==', '../images/tree-active.png','Pooth Khurd, Bawana'],
	['Jawaharlal Nehru Stadium', 28.582846, 77.234366, 'AallStationView5MinData.php?stName=SkxOU3RhZGl1bQ==', '../images/tree-active.png','Jawaharlal Nehru Stadium'],
	['Alipur', 28.815691, 77.152491, 'AallStationView5MinData.php?stName=QWxpcHVy', '../images/tree-active.png','Alipur'],
	['Sri Auribindo Marg', 28.528344, 77.189304, 'AallStationView5MinData.php?stName=U3JpQXVyYmluZG9NYXJn', '../images/tree-active.png','Sri Auribindo Marg'],
	['Pusa', 28.637371, 77.162879, 'AallStationView5MinData.php?stName=UHVzYQ==', '../images/tree-active.png','Pusa'],
	['Mundka', 28.682410, 77.030469, 'AallStationView5MinData.php?stName=TXVuZGth', '../images/tree-active.png','Mundka']
]

num = len(stations_from_dpcc)
dists = []

mins = []
for i in range(num):
    s1 = stations_from_dpcc[i]
    lat1 = s1[1]
    lng1 = s1[2]

    s1_min_dist = 1E10 # min dist of s1 to any other station

    for j in range(num):
        if i != j:
            s2 = stations_from_dpcc[j]
            lat2 = s2[1]
            lng2 = s2[2]

            dist = coord_distance(lat1, lng1, lat2, lng2)

            if dist < s1_min_dist:
                s1_min_dist = dist

    mins.append(s1_min_dist)

print(mins)
print("Min of mins:", min(mins), "m")
print("Max of mins:", max(mins), "m")
print("Mean:", np.mean(mins), "m")
print("std:", np.std(mins), "m")

"""
for i in range(num):
    s1 = stations_from_dpcc[i]
    lat1 = s1[1]
    lng1 = s1[2]
    for j in range(i + 1,num):
        s2 = stations_from_dpcc[j]
        lat2 = s2[1]
        lng2 = s2[2]
        dists.append( coord_distance(lat1, lng1, lat2, lng2) )

print("Min:",min(dists),"m")
print("Mean:",np.mean(dists),"m")
print("Median:",np.median(dists),"m")
print("Max:",max(dists),"m")
"""
