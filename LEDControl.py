import  RPi.GPIO as GPIO

def initiate(red_pin, green_pin, blue_pin, pwm_frequency):
    configure_board(red_pin, green_pin, blue_pin)
    pwms = configure_pwm(red_pin, green_pin, blue_pin, pwm_frequency)
    return pwms

def configure_board(red_pin, green_pin, blue_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red_pin, GPIO.OUT)
    GPIO.setup(green_pin, GPIO.OUT)
    GPIO.setup(blue_pin, GPIO.OUT)

def configure_pwm(red_pin, green_pin, blue_pin, pwm_frequency):
    pwm_red=GPIO.PWM(red_pin,pwm_frequency)
    pwm_green=GPIO.PWM(green_pin,pwm_frequency)
    pwm_blue=GPIO.PWM(blue_pin,pwm_frequency)

    pwm_red.start(0)
    pwm_green.start(0)
    pwm_blue.start(0)
    return [pwm_red, pwm_green, pwm_blue]

def check_value(value):
    if value > 255:
        return 255
    if value < 0:
        return 0
    return value

def set_red(value, pwm_red):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_RED, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_RED, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_red.ChangeDutyCycle(brightness)

def set_blue(value, pwm_blue):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_BLUE, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_BLUE, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_blue.ChangeDutyCycle(brightness)

def set_green(value, pwm_green):
    #value is ether "high", "low" or a number between 0-255
    if value == "high":
        GPIO.output(PIN_GREEN, GPIO.HIGH)
    elif value == "low":
        GPIO.output(PIN_GREEN, GPIO.LOW)
    else:
        value = check_value(value)
        brightness = 100 *(value / 255)
        pwm_green.ChangeDutyCycle(brightness)

def set_color(r,g,b, pwms):
    set_red(r, pwms[0])
    set_green(g, pwms[1])
    set_blue(b, pwms[2])
    
def cleanup():
    GPIO.cleanup()