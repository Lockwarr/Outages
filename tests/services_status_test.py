import unittest
from services_status import ongoingflappingOutages, flappingOutages

outages_no_flapping = [{"service_id": 1704, "duration": 2, "startTime": "2020-07-02  09:01:31"}, {"service_id": 2429, "duration": 1, "startTime": "2020-07-02  00:10:24"},
 {"service_id": 1704, "duration": 2, "startTime": "2020-07-02  00:18:31"}, {"service_id": 1704, "duration": 1, "startTime": "2020-07-02  00:49:31"},
 {"service_id": 2432, "duration": 2, "startTime": "2020-07-02  01:13:03"}, {"service_id": 1704, "duration": 1, "startTime": "2020-07-02  01:38:31"},
 {"service_id": 1704, "duration": 1, "startTime": "2020-07-02  03:53:31"}, {"service_id": 1223, "duration": 3, "startTime": "2020-07-02  04:03:44"},
 {"service_id": 1223, "duration": 9, "startTime": "2020-07-02  04:07:44"}, {"service_id": 1469, "duration": 4, "startTime": "2020-07-02  04:18:19"}]

outages_flapping = [{"service_id": 11, "duration": 2, "startTime": "2020-07-02  09:01:31"}, {"service_id": 11, "duration": 13, "startTime": "2020-07-02  10:01:31"},
 {"service_id": 21, "duration": 2, "startTime": "2020-07-02  00:18:31"}, {"service_id": 11, "duration": 1, "startTime": "2020-07-02  12:49:31"},
 {"service_id": 2432, "duration": 2, "startTime": "2020-07-02  01:13:03"}, {"service_id": 13, "duration": 1, "startTime": "2020-07-02  01:38:31"}]

multiple_outages_flapping = [{"service_id": 11, "duration": 2, "startTime": "2020-07-02  09:01:31"}, {"service_id": 11, "duration": 13, "startTime": "2020-07-02  10:01:31"},
 {"service_id": 21, "duration": 10, "startTime": "2020-07-02  00:18:31"}, {"service_id": 21, "duration": 5, "startTime": "2020-07-02  01:49:31"},
 {"service_id": 2432, "duration": 2, "startTime": "2020-07-02  01:13:03"}, {"service_id": 13, "duration": 1, "startTime": "2020-07-02  01:38:31"}]

outages_flapping_hours_passed = [{"service_id": 1704, "duration": 2, "startTime": "2020-07-02  09:01:31"}, {"service_id": 1704, "duration": 13, "startTime": "2020-07-02  10:01:31"},
 {"service_id": 1704, "duration": 2, "startTime": "2020-07-02  00:18:31"}, {"service_id": 2134, "duration": 1, "startTime": "2020-07-02  00:49:31"},
 {"service_id": 2432, "duration": 2, "startTime": "2020-07-02  01:13:03"}, {"service_id": 13, "duration": 1, "startTime": "2020-07-02  01:38:31"}]

current_outages_flapping = [{'service_id': 21, 'duration': 2, 'startTime': '2020-07-02  00:18:31', 'amountOfOutages': 1, 'endTime': '2020-07-02 00:20:31'},
 {'service_id': 2432, 'duration': 2, 'startTime': '2020-07-02  01:13:03', 'amountOfOutages': 1, 'endTime': '2020-07-02 01:15:03'}, 
 {'service_id': 13, 'duration': 1, 'startTime': '2020-07-02  01:38:31', 'amountOfOutages': 1, 'endTime': '2020-07-02 01:39:31'}, 
 {'service_id': 11, 'duration': 13, 'startTime': '2020-07-02  09:01:31', 'amountOfOutages': 2, 'endTime': '2020-07-02 09:14:31'}]

current_no_outages_flapping = [{'service_id': 21, 'duration': 2, 'startTime': '2020-07-02  00:18:31', 'amountOfOutages': 1, 'endTime': '2020-07-02 00:20:31'},
 {'service_id': 2432, 'duration': 2, 'startTime': '2020-07-02  01:13:03', 'amountOfOutages': 1, 'endTime': '2020-07-02 01:15:03'}, 
 {'service_id': 13, 'duration': 1, 'startTime': '2020-07-02  01:38:31', 'amountOfOutages': 1, 'endTime': '2020-07-02 01:39:31'}, 
 {'service_id': 11, 'duration': 16, 'startTime': '2020-07-02  09:01:31', 'amountOfOutages': 2, 'endTime': '2020-07-02 09:14:31'}]

class OngoingFlapping(unittest.TestCase):
    def test_no_ongoing_flapping(self):
        outages_time_sorted = sorted(outages_no_flapping, key = lambda i: i["startTime"]) 
        self.assertEqual(ongoingflappingOutages(outages_time_sorted, []), 0)
    def test_ongoing_flapping(self):
        outages_time_sorted = sorted(outages_flapping, key = lambda i: i["startTime"])
        self.assertEqual(ongoingflappingOutages(outages_time_sorted, []), 1)
    def test_multiple_ongoing_flapping(self):
        outages_time_sorted = sorted(multiple_outages_flapping, key = lambda i: i["startTime"])
        self.assertEqual(ongoingflappingOutages(outages_time_sorted, []), 2)
    def test_ongoing_flapping_once(self):
        outages_time_sorted = sorted(outages_flapping_hours_passed, key = lambda i: i["startTime"]) 
        self.assertEqual(ongoingflappingOutages(outages_time_sorted, []), 0)
    def test_no_ongoing_outages(self):
        self.assertEqual(ongoingflappingOutages([], []), 0)

class Flapping(unittest.TestCase):
    def test_flapping(self):
        outage = {"service_id": 11, "duration": 2, "startTime": "2020-07-02  10:01:31", "amountOfOutages": 1}
        ongoing_outages = []
        outages_time_sorted = sorted(current_outages_flapping, key = lambda i: i["startTime"])
        flappingOutages(ongoing_outages, outages_time_sorted, outage)
        self.assertEqual((len(ongoing_outages)), 1)
    def test_no_flapping(self):
        outage = {"service_id": 11, "duration": 2, "startTime": "2020-07-02  10:01:31", "amountOfOutages": 1}
        ongoing_outages = []
        outages_time_sorted = sorted(current_no_outages_flapping, key = lambda i: i["startTime"])
        flappingOutages(ongoing_outages, outages_time_sorted, outage)
        self.assertEqual((len(ongoing_outages)), 0)