import LEDControl as led
import time

class Fading:
    
    def __init__(self, pwms):
        self._running = True
        self.speed = 20
        self.pwms = pwms
        self.pwm_red = pwms[0]
        self.pwm_green = pwms[1]
        self.pwm_blue = pwms[2]
        self.fading_step = 3 #get-set missing

    def terminate(self):
        self._running = False
        
    def change_speed(self, value):
        self.speed = value
    
    def update_color(self, value):
        if value > 255:
            return 255
        if value < 0:
            return 0
        return value
        
    def fade_colors(self):
        red, green, blue = [255,0,0]
        led.set_color(red, green, blue, self.pwms)
        while self._running:
            if red == 255 and blue == 0 and green < 255:
                green = self.update_color(green + self.fading_step)
                led.set_green(green, self.pwm_green)
        
            elif green == 255 and blue == 0 and red > 0:
                red = self.update_color(red - self.fading_step)
                led.set_red(red, self.pwm_red)
            
            elif red == 0 and green == 255 and blue < 255:
                blue = self.update_color(blue + self.fading_step)
                led.set_blue(blue, self.pwm_blue)
            
            elif red == 0 and blue == 255 and green > 0:
                green = self.update_color(green - self.fading_step)
                led.set_green(green, self.pwm_green)
            
            elif green == 0 and blue == 255 and red < 255:
                red = self.update_color(red + self.fading_step)
                led.set_red(red, self.pwm_red)
            
            elif red == 255 and green == 0 and blue > 0:
                blue = self.update_color(blue - self.fading_step)
                led.set_blue(blue, self.pwm_blue)
            time.sleep(1/self.speed)