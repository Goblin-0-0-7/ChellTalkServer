from bluetooth import *
import time, sys
from threading import Thread
from datetime import datetime

sys.path.insert(0, "../")
#own Classes
import Alarm #not used ?
from AlarmClock import AlarmClock
import LEDControl as led
from lightshows.Fading import Fading
from lightshows.Stroboscope import Stroboscope
from MotionSensor import MotionSensor
from CO2Sensor import CO2Sensor

#default settings
red, green, blue = [0,0,0]

connection = False
motion_sensor_flag = False

#working with GPIO.BCM
PIN_RED = 27
PIN_GREEN = 22
PIN_BLUE = 17
PIN_MOTIONSENSOR_OUTPUT = 14


pwm_frequency = 100

pwms = led.initiate(PIN_RED, PIN_GREEN, PIN_BLUE, pwm_frequency)

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY)) #was PORT_ANY
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "ChellTalkServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
                    )

def open_socket(connection: bool, alarm_clock: AlarmClock, motion_sensor: MotionSensor, co2_sensor: CO2Sensor = None):
    while True:
        if(connection == False):
            print("Waiting for connection on RFCOMM channel %d" % port)
            client_sock, client_info = server_sock.accept()
            connection = True
            print("Accepted connection from ", client_info)
        try:
            data = client_sock.recv(1024).decode("ASCII")
            print("RECEIVED: %s" % data)
            
            if (data == "disconnect"):
                print("Client wanted to disconnect")
                client_sock.close()
                connection = False
                led.set_color(0,0,0)
            #fade
            elif ("-fade-" in data):
                led.set_color(0,0,0, pwms)
                fading = Fading(pwms)
                fade_thread = Thread(target = fading.fade_colors, args =( ), daemon = True)
                fade_thread.start()
            elif ("-fadeSpeed-" in data):
                msg = data.replace("-fadeSpeed-", "")
                try:
                    fading.change_speed(int(msg))
                except:
                    print("Couldn't change fading speed, fading probably not active.")
            elif ("-black-" in data):
                try:
                    fading.terminate()
                except:
                    print("Fading could not be terminated.")
                try:
                    strobe.terminate()
                except:
                    print("Stroboscope could not be terminated.")
                led.set_color(0,0,0, pwms)
            #strobe
            elif ("-strobe-" in data):
                strobe = Stroboscope(pwms)
                strobe_thread = Thread(target = strobe.run, args =( ), daemon = True)
                strobe_thread.start()
            elif ("-strobeFrequency-" in data):
                msg = data.replace("-strobeFrequency-", "")
                try:
                    strobe.change_frequency(int(msg))
                except:
                    print("Couldn't change fading speed, fading probably not active.")
            #rgb
            elif ("-rgbCode-" in data):
                msg = data.replace("-rgbCode-", "") #removing Tag
                red, green, blue, __ = msg.split(",",3)
                led.set_color(int(red), int(green), int(blue), pwms)
            #alarm
            elif ("-newTestAlarm-" in data):
                alarm_clock.new_test_alarm()
            elif ("-newAlarm-" in data):
                msg = data.replace("-newAlarm-", "")
                title, hour, min, sec, __ = msg.split(",",4)
                alarm_clock.new_alarm(title, [int(hour), int(min), int(sec)])
            elif ("-stopAlarm-" in data):
                alarm_clock.stop_alarms()
            #sensors
            elif ("-motionSensor-" in data):
                if (":activate" in data):
                    motion_sensor.activate()
                    motion_sensor_flag = True
                if (":deactivate" in data): #error when having the if statment as (":deactivate" in data and motion_sensor_flag)
                    if(motion_sensor_flag):
                        motion_sensor.deactivate()
                        motion_sensor_flag = False
            elif ("-co2Sensor-" in data):
                if (":calibrate" in data):
                    co2_sensor.calibrate()
        except IOError:
            print("Connection disconnected!")
            client_sock.close()
            connection = False
            led.set_color(0,0,0, pwms)
            pass
        except BluetoothError:
            print("Something wrong with bluetooth")
        except KeyboardInterrupt:
            print("\nDisconnected")
            client_sock.close()
            server_sock.close()
            led.set_color(0,0,0, pwms)
            led.cleanup()
            break
    
def main():
    alarm_clock = AlarmClock()
    alarm_clock_thread = Thread(target = alarm_clock.run, args =( ), daemon = True)
    alarm_clock_thread.start()

    # no co2 sensor on pi
    # co2_sensor = CO2Sensor()
    # co2_sensor_thread = Thread(target = co2_sensor.run, args= ( ), daemon = True)
    # co2_sensor_thread.start()
    
    motion_sensor = MotionSensor(PIN_MOTIONSENSOR_OUTPUT, pwms)
    
    open_socket(connection,
                alarm_clock,
                motion_sensor,
                #co2_sensor
                )
    exit()
    
if __name__ == "__main__":
    main()

