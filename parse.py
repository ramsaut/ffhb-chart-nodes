#! /usr/bin/env python
import json
import dateutil.parser
import urllib2
FILTER_BY_GPS = True
WALLE_LON_MIN = 8.757305145263672
WALLE_LON_MAX = 8.796873092651367
WALLE_LAT_MIN = 53.087546501208976
WALLE_LAT_MAX = 53.108470468690165
f = urllib2.urlopen(
    "https://downloads.bremen.freifunk.net/data/nodes.json")
csv = open("firstseen.csv", 'w')
if FILTER_BY_GPS:
    csv.write("node;hostname;firstseen;latitude;longitude\n")
else:
    csv.write("node;hostname;firstseen\n")
js = open("data.js", 'w')
data = json.loads(f.read())
data = data['nodes']
js.write("DATA = [\n")
a = []
totalclients = 0
for node in data:
    if FILTER_BY_GPS:
        if 'location' in data[node]['nodeinfo'].keys():
            firstseen = data[node]['firstseen']
            latitude = data[node]['nodeinfo']['location']['latitude']
            longitude = data[node]['nodeinfo']['location']['longitude']
            hostname = data[node]['nodeinfo']['hostname']
            clients = data[node]['statistics']['clients']
            if((latitude > WALLE_LAT_MIN) and (latitude < WALLE_LAT_MAX) and
                    (longitude > WALLE_LON_MIN) and
                    (longitude < WALLE_LON_MAX)):
                a.append(firstseen)
                totalclients += clients
                csv.write(node +
                          ";" + hostname +
                          ";" + firstseen +
                          ";" + str(latitude) +
                          ";" + str(longitude) +
                          ";" + str(clients) + "\n")
    else:
        a.append(data[node]['firstseen'])
        totalclients += data[node]['statistics']['clients']
        csv.write(node +
                  ";" + data[node]['nodeinfo']['hostname'] +
                  ";" + data[node]['firstseen'] +
                  ";" + str(data[node]['statistics']['clients']) + "\n")

a = sorted(a)
current = 0

for firstseen in a:
    firstseen = dateutil.parser.parse(firstseen)
    current = current + 1
    year = firstseen.year
    month = firstseen.month
    day = firstseen.day
    js.write("{x: new Date(" + str(year) + "," + str(month) +
             "," + str(day) + "), y: " + str(current) + "},\n")

js.write("]\n")
js.write("clients = "+str(totalclients))
