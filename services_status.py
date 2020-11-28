# filename: services_status.py
"""Functionality of outages api"""
import hug
import json
from datetime import datetime
from datetime import timedelta


def ongoingflappingOutages(outages_time_sorted, ongoing_outages):
    current_flapping_outages = []
    for outage in outages_time_sorted:
        if outage["duration"]<15:
            id = outage["service_id"]
            start_datetime = datetime.strptime(outage["startTime"], '%Y-%m-%d %H:%M:%S')
            end_datetime = start_datetime + timedelta(minutes=outage["duration"])
            #check if 3 hours have passed for any ongoing_outage
            ongoing_flapping_outage = next((item for item in ongoing_outages if item["service_id"] == id), None)
            if ongoing_flapping_outage:
                end_time_ongoing = datetime.strptime(ongoing_flapping_outage["endTime"], '%Y-%m-%d %H:%M:%S')
                if (start_datetime - end_time_ongoing).seconds >= 10800:
                    ongoing_outages[:] = [o for o in ongoing_outages if o.get("service_id") != id]
                elif (start_datetime - end_time_ongoing).seconds < 10800 and (start_datetime - end_time_ongoing).seconds > 0:
                    ongoing_flapping_outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
            flappingOutages(ongoing_outages, current_flapping_outages, outage)
    return len(ongoing_outages)

def flappingOutages(ongoing_outages, current_flapping_outages, outage):
    start_datetime = datetime.strptime(outage["startTime"], '%Y-%m-%d %H:%M:%S')
    end_datetime = start_datetime + timedelta(minutes=outage["duration"])
    #check if service exists in current_flapping_outages keys
    flapping_outage = next((item for item in current_flapping_outages if item["service_id"] == outage["service_id"]), None)
    if flapping_outage:
        flapping_start_datetime = datetime.strptime(flapping_outage["startTime"], '%Y-%m-%d %H:%M:%S')
        duration_sum = flapping_outage["duration"] + outage["duration"]
        if (end_datetime - flapping_start_datetime).seconds <= 7200 and duration_sum < 15:
            flapping_outage["duration"] = duration_sum
            flapping_outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
            flapping_outage["amountOfOutages"] += 1
            #it's unclear what sumOfOutages should be
            #flapping_outages[id]["sumOfOutages"] =    
        elif (end_datetime - flapping_start_datetime).seconds >= 7200 and outage["duration"] < 15:
            flapping_outage = outage
            flapping_outage["amountOfOutages"] = 1
            flapping_outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
        elif duration_sum == 15:
            flapping_outage["amountOfOutages"] += 1
            flapping_outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
            flapping_outage["duration"] = duration_sum
            ongoing_outages.append(flapping_outage)
    else:
        outage["amountOfOutages"] = 1
        outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
        current_flapping_outages.append(outage)

def calculateDownOutages(past_days, outages):
    currentOutages = []
    now = datetime.now()
    for outage in outages:
        start_datetime = datetime.strptime(outage["startTime"], '%Y-%m-%d %H:%M:%S')
        end_datetime = start_datetime + timedelta(minutes=outage["duration"])
        if past_days != 0:
            since = now - timedelta(days=past_days)
            if start_datetime >= since:
                outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
                currentOutages.append(outage)
        else:
            if start_datetime <= now and now <= end_datetime:
                outage["endTime"] = end_datetime.strftime('%Y-%m-%d %H:%M:%S')
                currentOutages.append(outage)
    return currentOutages