import json

class Alarm(dict):

    def __init__(self, title, alarm_date, alarm_time, alarm_repetition =None, soundfile =None, lightshow =None):
        self._running = False

        self.title = title
        self.alarm_date = alarm_date
        self.alarm_time = alarm_time #array with [HH,MM,SS]
        self.alarm_repetition = alarm_repetition
        self.soundfile = soundfile
        self.lightshow = lightshow

        self.props = self.create_dict()

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
        with open("alarms\{0}.json".format(self.title), "w") as outfile:
            outfile.write(file)

    def go_off(self):
        self._running = True
        while self._running:
            print("Beeep")
            #playsound('D:/Library/Documents/Projects/Coding/Beginner Python Projects/Alarm Clock/alarm.wav')
        

    def stop(self):
        self._running = False
