from bluetooth import *
import time, sys
from threading import Thread
from datetime import datetime

sys.path.insert(0, "../")
#own Classes
import Alarm
from AlarmClock import AlarmClock
import LEDControl as led
from lightshows.Fading import Fading
from lightshows.Stroboscope import Stroboscope
#default settings
red, green, blue = [0,0,0]

connection = False

PIN_RED = 27
PIN_GREEN = 22
PIN_BLUE = 17

pwm_frequency = 100

pwms= led.initiate(PIN_RED, PIN_GREEN, PIN_BLUE, pwm_frequency)

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
                led.set_color(0,0,0)
            elif ("-fade-" in data):
                print("RECEIVED: %s" % data)
                led.set_color(0,0,0, pwms)
                fading = Fading(pwms)
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
                try:
                    strobe.terminate()
                except:
                    print("Stroboscope could not be terminated.")
                led.set_color(0,0,0, pwms)
            elif ("-strobe-" in data):
                print("RECEIVED: %s" % data)
                strobe = Stroboscope(pwms)
                strobe_thread = Thread(target = strobe.run, args =( ), daemon = True)
                strobe_thread.start()
            elif ("-strobeFrequency-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-strobeFrequency-", "")
                try:
                    strobe.change_frequency(int(msg))
                except:
                    print("Couldn't change fading speed, fading probably not active.")
            elif ("-rgbCode-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-rgbCode-", "") #removing Tag
                red, green, blue, __ = msg.split(",",3)
                led.set_color(int(red), int(green), int(blue), pwms)
            elif ("-newTestAlarm-" in data):
                alarm_clock.new_test_alarm()
            elif ("-newAlarm-" in data):
                print("RECEIVED: %s" % data)
                msg = data.replace("-newAlarm-", "")
                title, hour, min, sec, __ = msg.split(",",4)
                alarm_clock.new_alarm(title, [int(hour), int(min), int(sec)])
            elif ("-stopAlarm-" in data):
                alarm_clock.stop_alarms()
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
    open_socket(connection, alarm_clock)
    exit()
    
if __name__ == "__main__":
    main()

