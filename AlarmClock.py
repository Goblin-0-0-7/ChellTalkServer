from datetime import datetime
from Alarm import Alarm
import json
import os

class AlarmClock:

    def __init__(self):
        self._running = True
        self.alarm_folder = "alarms/"
        self.alarm_list = []
        self.load_alarms()

    def terminate(self):
        self._running = False
    
    def new_alarm(self, title, alarm_time, alarm_date =None, alarm_repetition =None, soundfile =None, lightshow =None):
        now = datetime.now()
        if not alarm_date:
            year = int(now.strftime("%Y"))
            month = int(now.strftime("%m"))
            day = int(now.strftime("%d"))
            alarm_date = [year,month,day]

        new = Alarm(title, alarm_date, alarm_time, alarm_repetition, soundfile, lightshow)
        self.alarm_list.append(new)
        new.save()

    def load_alarms(self):
        alarm_paths = os.listdir(self.alarm_folder)
        for element in alarm_paths:
            try:
                with open(self.alarm_folder + element, "r") as infile:
                    alarm_json = json.load(infile)
                    current_alarm = Alarm(alarm_json["title"], alarm_json["alarm_date"], alarm_json["alarm_time"], alarm_json["alarm_repetition"], alarm_json["soundfile"], alarm_json["lightshow"])
                    self.alarm_list.append(current_alarm)
            except:
                print("The file {0} is not a json, this file should not be in the alarms folder".format(element))

    def run(self):
        while self._running:
            now = datetime.now()

            current_year = now.strftime("%Y")
            current_month = now.strftime("%m")
            current_day = now.strftime("%d")
            current_hour = now.strftime("%I")
            current_min = now.strftime("%M")
            current_sec = now.strftime("%S")

            for element in self.alarm_list:
                if element.alarm_date[0] == int(current_year):
                    if element.alarm_date[1] == int(current_month):
                        if element.alarm_date[2] == int(current_day):
                            if element.alarm_time[0] == int(current_hour):
                                if element.alarm_time[1] == int(current_min):
                                    if element.alarm_time[2] == int(current_sec):
                                        if not element._running:
                                            element.go_off()