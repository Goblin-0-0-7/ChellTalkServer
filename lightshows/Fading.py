import time

class Fading:
    
    def __init__(self, server, fading_step):
        self._running = True
        self.speed = 20
        self.server = server
        self.fading_step = fading_step

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
        self.server.set_color(red, green, blue)
        while self._running:
            if red == 255 and blue == 0 and green < 255:
                green = self.update_color(green + self.fading_step)
                self.server.set_green(green)
        
            elif green == 255 and blue == 0 and red > 0:
                red = self.update_color(red - self.fading_step)
                self.server.set_red(red)
            
            elif red == 0 and green == 255 and blue < 255:
                blue = self.update_color(blue + self.fading_step)
                self.server.set_blue(blue)
            
            elif red == 0 and blue == 255 and green > 0:
                green = self.update_color(green - self.fading_step)
                self.server.set_green(green)
            
            elif green == 0 and blue == 255 and red < 255:
                red = self.update_color(red + self.fading_step)
                self.server.set_red(red)
            
            elif red == 255 and green == 0 and blue > 0:
                blue = self.update_color(blue - self.fading_step)
                self.server.set_blue(blue)
            time.sleep(1/self.speed)