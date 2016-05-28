#! /usr/bin/env python
import json
import dateutil.parser
import urllib2
WALLE_LON_MIN = 8.757305145263672
WALLE_LON_MAX = 8.796873092651367
WALLE_LAT_MIN = 53.087546501208976
WALLE_LAT_MAX = 53.108470468690165
f = urllib2.urlopen(
    "https://downloads.bremen.freifunk.net/data/nodes.json")
js = open("data.js", 'w')
data = json.loads(f.read())
data = data['nodes']
WALLE = []
BRE = []
totalclients = 0
clientsWALLE = 0
for node in data:
    if 'location' in data[node]['nodeinfo'].keys():
        firstseen = data[node]['firstseen']
        latitude = data[node]['nodeinfo']['location']['latitude']
        longitude = data[node]['nodeinfo']['location']['longitude']
        hostname = data[node]['nodeinfo']['hostname']
        clients = data[node]['statistics']['clients']
        if((latitude > WALLE_LAT_MIN) and (latitude < WALLE_LAT_MAX) and
                (longitude > WALLE_LON_MIN) and
                (longitude < WALLE_LON_MAX)):
            WALLE.append(firstseen)
            clientsWALLE += data[node]['statistics']['clients']
    BRE.append(data[node]['firstseen'])
    totalclients += data[node]['statistics']['clients']

WALLE = sorted(WALLE)
BRE = sorted(BRE)


def toJS(data, label, file):
    file.write(label + " = [\n")
    current = 0
    for firstseen in data:
        firstseen = dateutil.parser.parse(firstseen)
        current = current + 1
        year = firstseen.year
        month = firstseen.month
        day = firstseen.day
        file.write("{x: new Date(" + str(year) + "," + str(month) +
                    "," + str(day) + "), y: " + str(current) + "},\n")
    file.write("]\n")

toJS(WALLE, "WALLE", js)
toJS(BRE, "BRE", js)


js.write("clients = " + str(totalclients) + "\n")
js.write("clientsWALLE = " + str(clientsWALLE) + "\n")
