
# filename: services_status.py
"""Outages api written using hug"""
import hug
import json
from datetime import datetime
from services_status import calculateDownOutages, ongoingflappingOutages

ongoing_outages = []
outages = []

with open('outages.txt', 'r') as data_file:
    json_data = data_file.read()
if json_data:
    outages = json.loads(json_data)

@hug.post('/add_outage')
def addOutage(body):
    """Adds an outage record"""
    if "duration" not in body or "timestamp" not in body or "service_id" not in body:
        return "service_id, duration and timestamp are required in body"
    outage = {"service_id": body["service_id"], "duration": body["duration"],
              "startTime": datetime.fromtimestamp(body["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')}
    outages.append(outage)
    return "Outage has been added"

@hug.get('/currently_down')
def currentlyDownServices():
    """Check for currently down outages"""
    return calculateDownOutages(0, outages)

@hug.get('/recently_down')
def recentlyDownServices(days:hug.types.number):
    """Check for recently down outages passing how many days back to look for"""
    return calculateDownOutages(days, outages)

@hug.get('/ongoing_flapping_outages')
def ongoingOutages():
    """Check for ongoing flapping scenarios"""
    if outages:
        outages_time_sorted = sorted(outages, key = lambda i: i["startTime"])
        ongoingflappingOutages(outages_time_sorted, ongoing_outages)
    return ongoing_outages