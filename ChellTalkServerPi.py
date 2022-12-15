from bluetooth import *
import  RPi.GPIO as GPIO
import time
from threading import Thread
from datetime import datetime
from AlarmClock import AlarmClock

#own Classes
import Alarm

#changable variables (by user)
fading_step = 3
#default settings
red, green, blue = [0,0,0]

connection = False

GPIO.setmode(GPIO.BCM)
PIN_RED = 27
PIN_GREEN = 22
PIN_BLUE = 17

GPIO.setup(PIN_BLUE, GPIO.OUT)
GPIO.setup(PIN_GREEN, GPIO.OUT)
GPIO.setup(PIN_RED, GPIO.OUT)

pwm_frequenzy = 100
pwm_red=GPIO.PWM(PIN_RED,pwm_frequenzy)
pwm_blue=GPIO.PWM(PIN_BLUE,pwm_frequenzy)
pwm_green=GPIO.PWM(PIN_GREEN,pwm_frequenzy)

pwm_red.start(0)
pwm_blue.start(0)
pwm_green.start(0)

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "ChellTalkServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
                    )

def check_value(value):
    if value > 255:
        return 255
    if value < 0:
        return 0
    return value

def set_red(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_RED, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_RED, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_red.ChangeDutyCycle(brightness)

def set_blue(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_BLUE, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_BLUE, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_blue.ChangeDutyCycle(brightness)

def set_green(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_GREEN, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_GREEN, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_green.ChangeDutyCycle(brightness)

def set_color(r,g,b):
    set_red(r)
    set_green(g)
    set_blue(b)
    
class Fading:
    
    def __init__(self):
        self._running = True
        self.speed = 20

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
        set_color(red, green, blue)
        while self._running:
            if red == 255 and blue == 0 and green < 255:
                green = self.update_color(green + fading_step)
                set_green(green)
        
            elif green == 255 and blue == 0 and red > 0:
                red = self.update_color(red - fading_step)
                set_red(red)
            
            elif red == 0 and green == 255 and blue < 255:
                blue = self.update_color(blue + fading_step)
                set_blue(blue)
            
            elif red == 0 and blue == 255 and green > 0:
                green = self.update_color(green - fading_step)
                set_green(green)
            
            elif green == 0 and blue == 255 and red < 255:
                red = self.update_color(red + fading_step)
                set_red(red)
            
            elif red == 255 and green == 0 and blue > 0:
                blue = self.update_color(blue - fading_step)
                set_blue(blue)
            time.sleep(1/self.speed)

def open_socket(connection: bool, alarm_clock: AlarmClock):
    while True:
        if(connection == False):
            print("Waiting for connection on RFCOMM channel %d" % port)
            client_sock, client_info = server_sock.accept()
            connection = True
            print("Accepted connection from ", client_info)
        try:
            data = client_sock.recv(1024).decode("ASCII")

            if (data == "disconnect"):
                print("Client wanted to disconnect")
                client_sock.close()
                connection = False
                set_color(0,0,0)
            elif ("-fade-" in data):
                print("RECEIVED: %s" % data)
                set_color(0,0,0)
                fading = Fading()
                fade_thread = Thread(target = fading.fade_colors, args =( ), daemon = True)
                fade_thread.start()
            elif ("-fadeSpeed-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-fadeSpeed-", "")
                try:
                    fading.change_speed(int(msg))
                except:
                    print("Couldn't change fading speed, fading probably not active.")
            elif ("-black-" in data):
                print("RECEIVED: %s" % data)
                try:
                    fading.terminate()
                except:
                    print("Fading could not be terminated.")
                set_color(0,0,0)
            elif ("-rgbCode-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-rgbCode-", "") #removing Tag
                red, green, blue, __ = msg.split(",",3)
                set_color(int(red), int(green), int(blue))
            elif ("-newTestAlarm-" in data):
                alarm_clock.new_test_alarm()
            elif ("-newAlarm-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-newAlarm-", "")
                title, hour, min, sec, mo, di, mi, do, fr, sa , so, __ = msg.split(",",11)
                alarm_clock.new_alarm(title, [int(hour), int(min), int(sec)], alarm_repetition=[int(mo), int(di), int(mi), int(do), int(fr), int(sa), int(so)])
            elif ("-stopAlarm-" in data):
                alarm_clock.stop_alarms()
        except IOError:
            print("Connection disconnected!")
            client_sock.close()
            connection = False
            set_color(0,0,0)
            pass
        except BluetoothError:
            print("Something wrong with bluetooth")
        except KeyboardInterrupt:
            print("\nDisconnected")
            client_sock.close()
            server_sock.close()
            set_color(0,0,0)
            GPIO.cleanup()
            break
    
def main():
    alarm_clock = AlarmClock()
    alarm_clock_thread = Thread(target = alarm_clock.run, args =( ), daemon = True)
    alarm_clock_thread.start()
    open_socket(connection, alarm_clock)
    exit()
    
if __name__ == "__main__":
    main()
