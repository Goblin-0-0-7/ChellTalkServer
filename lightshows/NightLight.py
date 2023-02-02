import LEDControl as led
import time

class NightLight:
    
    def __init__(self, pwms, length: int =20, color: list =[255,255,255]):
        self.stop = False
        self.length = length
        self.pwms = pwms
        self.pwm_red = pwms[0]
        self.pwm_green = pwms[1]
        self.pwm_blue = pwms[2]
        self.red_max = color[0]
        self.green_max = color[1]
        self.blue_max = color[2]
        
    def start(self):
        self.stop = False
    
    def terminate(self):
        self.stop = True

    def get_status(self):
        return not self.stop

    def run(self):
        time_start = time.time()
        time_end = time_start + self.length
        while time.time() <= time_end:
            delta_time = time.time() - time_start
            next_red = -(self.red_max/self.length) * delta_time + self.red_max
            next_green = -(self.green_max/self.length) * delta_time + self.green_max
            next_blue = -(self.blue_max/self.length) * delta_time + self.blue_max
            led.set_color(next_red, next_green, next_blue, self.pwms)
            time.sleep(1/500)
            if self.stop:
                break
        led.set_color(0,0,0, self.pwms)
        self.stop = True