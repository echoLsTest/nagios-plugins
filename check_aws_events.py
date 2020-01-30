#!/usr/bin/python
import sys
import json
import boto3
import time
import argparse
from dateutil.parser import parse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Monitor AWS event logs.')
parser.add_argument('-s', '--service', help='Check the mentioned service.')
parser.add_argument('-r', '--region', help='Check in the mentioned region.')
args = parser.parse_args()

def get_describe_event():
    health = boto3.client('health')
    response = health.describe_events(
        filter={
            'regions': [args.region],
            'services': [args.service],
            'eventStatusCodes': ['open', 'upcoming']
        }
    )
    return response

screened_events = []
event_type = []
result = get_describe_event()
results = json.dumps(result, indent=3, sort_keys=True, default=str)
parsed_data = json.loads(results)

def check_events(event_1, event_2):
    return event_1["eventTypeCode"] == event_2["eventTypeCode"] and event_1["region"] == event_2["region"]

if parsed_data["events"]:
    for parsed_event in parsed_data["events"]:
        present = False
        for event_index in range(len(screened_events)):
            if check_events(parsed_event, screened_events[event_index]):
                present = True
                parsed_events_date = parse(parsed_event["startTime"])
                event_date = parse(screened_events[event_index]["startTime"])
                if parsed_events_date > event_date:
                    screened_events[event_index] = parsed_event
        if not present:
            screened_events.append(parsed_event)

    for event in screened_events:
        if event:
            event_type.append(event['eventTypeCode'])

    screened_events = {"events": screened_events}
    last_posted_date = abs(datetime.now() - event_date.replace(tzinfo=None))

    if last_posted_date.days < 10:
        print ("WARNING - Attention needed for %s" % (event['eventTypeCode']))
    elif last_posted_date.days > 10:
        print ("CRITICAL - Attention needed for %s" % (event['eventTypeCode']))

else:
    print("OK - No new notifications for %s service" % (args.service))
