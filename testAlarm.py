from datetime import datetime
from Alarm import Alarm
import json

class AlarmClock:

    def __init__(self):
        self._running = True
        self.alarm_list = []
        #load all saved Alarms os.walk (Title-AlarmTitle)
        #create Alarm objs

    def terminate(self):
        self._running = False
    
    def new_alarm(self, title, alarm_time, alarm_date =None, alarm_repetition =None, soundfile =None, lightshow =None):
        now = datetime.now()
        if not alarm_date:
            year = now.strftime("%Y")
            month = now.strftime("%m")
            day = now.strftime("%d")
            alarm_date = [year,month,day]

        new = Alarm(title, alarm_date, alarm_time, alarm_repetition, soundfile, lightshow)
        self.alarm_list.append(new)
        new.save()

    def load_alarm(self):
        ...

    def run(self):
        while self._running:
            now = datetime.now()

            current_hour = now.strftime("%I")
            current_min = now.strftime("%M")
            current_sec = now.strftime("%S")
            current_period = now.strftime("%p")
            #interate throught alarm objs
            """
            if alarm_period == current_period:
                if alarm_hour == current_hour:
                    if alarm_min == current_min:
                        if alarm_sec == current_sec:
                            print("Wake Up!")
                            playsound('D:/Library/Documents/Projects/Coding/Beginner Python Projects/Alarm Clock/alarm.wav')
                            break
            """
a = AlarmClock()
a.new_alarm("testAlarm", [4, 20, 00])
print(datetime.now().strftime("%H"))