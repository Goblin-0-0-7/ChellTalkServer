import  RPi.GPIO as GPIO
from threading import Thread

from lightshows.NightLight import NightLight

class MotionSensor:

    def __init__(self, gpio, pwms, action: str ="nigth-light"):
        self.gpio = gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio, GPIO.IN)
        self.state = self.__get_state()
        self.action = action
        self.pwms = pwms # not nice code

    def __get_state(self):
        return GPIO.input(self.gpio)

    def activate(self):
        GPIO.add_event_detect(self.gpio, GPIO.BOTH, callback=self.edge_callback)#, bouncetime=1) if sensor changes input to fast 
        self.state = self.__get_state()

    def deactivate(self):
        GPIO.remove_event.detect(self.gpio)

    def edge_callback(self):
        state = self.__get_state()
        if state != self.state:
            if state == 1: # edge 0=>1
                self.act()
            else: # edge 1=>0
                pass
            self.state = state

    def motion_detected(self):
        self.state = self.__get_state()
        return self.state == 1

    def act(self):
        if self.action == "night-light":
            niLi = NightLight(self.pwms)
            niLi_thread = Thread(target = niLi.run, args =( ), daemon = True)
            niLi_thread.join()
