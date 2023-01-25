import LEDControl as led
import time

class Stroboscope:
    
    def __init__(self, pwms, frequency: int =20, color: str ="white"):
        self._running = True
        self.pwms = pwms
        self.pwm_red = pwms[0]
        self.pwm_green = pwms[1]
        self.pwm_blue = pwms[2]
        self.frequency = frequency
        self.set_color(color)

    def terminate(self):
        self._running = False
        
    def change_frequency(self, value):
        #in Hz
        self.frequency = value
    
    def set_color(self, color: str ="white"):
        if color == "red":
            self.red = 255
            self.green = 0
            self.blue = 0
        elif color == "green":
            self.red = 0
            self.green = 255
            self.blue = 0
        elif color == "blue":
            self.red = 0
            self.green = 0
            self.blue = 255
        else: #defaults to white
            self.red = 255
            self.green = 255
            self.blue = 255
        
    def run(self):
        while self._running:
            led.set_color(self.red, self.green, self.blue, self.pwms)
            time.sleep(1/self.frequency)
            led.set_color(0,0,0, self.pwms)
            time.sleep(1/self.frequency)