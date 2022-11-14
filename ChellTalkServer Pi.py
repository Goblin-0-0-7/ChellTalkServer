from bluetooth import *
import  RPi.GPIO as GPIO
import time
from threading import Thread

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

connection = False
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

def set_red(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_RED, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_RED, GPIO.LOW)
    else:
        brightness = 100 *(value / 255)
        #brightness = pwm_frequenzy *(value / 255)
        pwm_red.ChangeDutyCycle(brightness)

def set_blue(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_BLUE, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_BLUE, GPIO.LOW)
    else:
        brightness = 100 *(value / 255)
        pwm_blue.ChangeDutyCycle(brightness)

def set_green(value):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_GREEN, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_GREEN, GPIO.LOW)
    else:
        brightness = 100 *(value / 255)
        pwm_green.ChangeDutyCycle(brightness)

def set_color(r,g,b):
    set_red(r)
    set_green(g)
    set_blue(b)
    
class Fading:
    
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def fade_colors(self, speed: int =1):
        while self._running:
            print("Thread running")
            time.sleep(5)

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
        elif (data == "fade"):
            print("RECEIVED: %s" % data)
            fading = Fading()
            fade_thread = Thread(target = fading.fade_colors, args =(True, ), daemon = True)
            fade_thread.start()
        elif (data == "black"):
            print("RECEIVED: %s" % data)
            fading.terminate()
            set_color(0,0,0)
        else:
            rgb_value = data.split(",",3)
            set_color(int(rgb_value[0]), int(rgb_value[1]), int(rgb_value[2]))
            print("RECEIVED: %s" % data)
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

