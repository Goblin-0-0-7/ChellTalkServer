import LEDControl as led
import time

class NightLight:
    
    def __init__(self, pwms, length: int =20, color: list =[255,255,255]):
        self.pwms = pwms
        self.pwm_red = pwms[0]
        self.pwm_green = pwms[1]
        self.pwm_blue = pwms[2]
        self.red_max = color[0]
        self.green_max = color[1]
        self.blue_max = color[2]

    def run(self):
        time_end = time.time() + self.length
        while time.time() <= time_end:
            next_red = -(self.red_max/self.length) * time.time() + self.red_max
            next_green = -(self.green_max/self.length) * time.time() + self.green_max
            next_blue = -(self.blue_max/self.length) * time.time() + self.blue_max
            led.set_color(next_red, next_green, next_blue, self.pwms)
        led.set_color(0,0,0, self.pwms)