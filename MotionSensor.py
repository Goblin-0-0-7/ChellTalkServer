import  RPi.GPIO as GPIO
from threading import Thread

import LEDControl as led
from lightshows.NightLight import NightLight

class MotionSensor:

    def __init__(self, gpio, pwms, action: str ="night-light"):
        self.gpio = gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio, GPIO.IN)
        self.state = self.__get_state()
        self.action = action
        self.pwms = pwms # not nice code
        self.acting = False

    def __get_state(self):
        return GPIO.input(self.gpio)

    def activate(self):
        self.niLi = NightLight(self.pwms)
        self.niLi.start()
        GPIO.add_event_detect(self.gpio, GPIO.BOTH, callback=self.edge_callback)#, bouncetime=1) if sensor changes input to fast 
        self.state = self.__get_state()

    def deactivate(self):
        GPIO.remove_event_detect(self.gpio)
        self.niLi.terminate()

    def edge_callback(self, channel):
        state = self.__get_state()
        if state != self.state:
            if state == 1 and not self.acting: # edge 0=>1
                print("Motion Detected")
                self.act()
            else: # edge 1=>0
                pass
            self.state = state

    def motion_detected(self):
        self.state = self.__get_state()
        return self.state == 1

    def act(self):
        if (self.niLi.get_status):
            if self.action == "night-light":
                niLi_thread = Thread(target = self.niLi.run, args =( ), daemon = True)
                niLi_thread.start()
        