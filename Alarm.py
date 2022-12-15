import json
import numpy as np
import datetime
from datetime import date
from pygame import mixer

class Alarm():

    def __init__(self, title: str, alarm_date: list, alarm_time: list, alarm_repetition: list =[0,0,0,0,0,0,0], soundfile: str =None, lightshow: str =None):
        self._running = False

        self.title = title
        self.alarm_date = alarm_date
        self.alarm_time = alarm_time #array with [HH,MM,SS]
        self.alarm_repetition = alarm_repetition #array of the structure [mo,di,mi,do,fr,sa,so] alarm goes off if element at mo,di etc. is set to 1
        self.soundfile = soundfile
        self.lightshow = lightshow

        self.props = self.create_dict()

        mixer.init()

    def create_dict(self):
        props = {
            "title": self.title,
            "alarm_date": self.alarm_date,
            "alarm_time": self.alarm_time,
            "alarm_repetition": self.alarm_repetition,
            "soundfile": self.soundfile,
            "lightshow": self.lightshow
        }
        return props

    def save(self):
        file = json.dumps(self.props)
        with open("alarms/{0}.json".format(self.title), "w") as outfile:
            outfile.write(file)

    def set_next_alarm(self):
        today = date.today()
        day_of_week = today.weekday()
        try:
            week_part_1, week_part_2, __ = np.split(np.array(self.alarm_repetition), [day_of_week + 1,7])
        except IndexError:
            week_part_1 = np.array(self.alarm_repetition)
            week_part_2 = None

        try:
            week_index = np.where(week_part_2 == 1)[0][0] #get the first match
            next_day = week_index + week_part_1.size
        except ValueError:
            next_day = None
        except IndexError:
            next_day = None
        
        if next_day == None:
            try:
                next_day = np.where(week_part_1 == 1)[0][0]
            except ValueError:
                next_day = None
            except IndexError:
                next_day = None
        if next_day:
            next_alarm_date = today + datetime.timedelta(days=-today.weekday() + next_day, weeks=1)
            self.alarm_date = [next_alarm_date.strftime("%H"), next_alarm_date.strftime("%M"), next_alarm_date.strftime("%S")]

    def play_alarm(self, soundfile: str =""):
        if soundfile == "":
            mixer.music.load("alarmsounds/Marc Rebillet - Your New Morning Alarm.mp3")
        else:
            path = "alarmsounds/" + soundfile
            mixer.music.load(path)
        mixer.music.set_volume(0.9)
        mixer.music.play()

    def go_off(self):
        self._running = True
        self.set_next_alarm()
        self.play_alarm()
        
    def stop(self):
        mixer.music.stop()
        self._running = False
