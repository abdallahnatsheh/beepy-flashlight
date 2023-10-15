import RPi.GPIO as GPIO
import datetime
import os
import time

BUTTON_PIN = 17

SHORT_PRESS_TIME = 0.5  # Less than 0.5 seconds
REPEAT_TIMEOUT = 0.5  # Repeat short presses should be within 1s
MEDIUM_PRESS_TIME = 2  # Less than 2.0 seconds

SHORT_PRESS_COUNT = 0
BUTTON_PRESS_TIME = 0
BUTTON_RELEASE_TIME = 0
LED_ON = False  # Use a boolean variable to track LED state

def my_callback(channel):
    global BUTTON_PRESS_TIME
    global SHORT_PRESS_COUNT
    global BUTTON_RELEASE_TIME
    global LED_ON  # Use the global variable to track LED state

    now = time.time()
    if GPIO.input(channel):
        button_duration = now - BUTTON_PRESS_TIME

        if 0.01 <= button_duration < SHORT_PRESS_TIME:  # Short Press
            SHORT_PRESS_COUNT += 1

            # Toggle the LED state on a short press
            LED_ON = not LED_ON
            if LED_ON:
                set_white_led()
            else:
                turn_off_led()

        BUTTON_RELEASE_TIME = now
    else:
        BUTTON_PRESS_TIME = now

def handle_press():
    global SHORT_PRESS_COUNT
    global BUTTON_RELEASE_TIME
    global BUTTON_PRESS_TIME
    # Remove the LED_ON global variable since we're tracking it in my_callback now

    now = time.time()

    while not GPIO.input(BUTTON_PIN):  # Button is being held
        now = time.time()
        if SHORT_PRESS_COUNT >= 3:
            turn_off_led()

    if SHORT_PRESS_COUNT == 2:
        with open('/sys/firmware/beepy/led_red', 'w') as red:
            red.write("128")
        with open('/sys/firmware/beepy/led_green', 'w') as green:
            green.write("70")
        with open('/sys/firmware/beepy/led_blue', 'w') as blue:
            blue.write("0")
        if now - BUTTON_RELEASE_TIME > REPEAT_TIMEOUT:
            execute_script('short_press_2.sh')

    if SHORT_PRESS_COUNT == 1:
        with open('/sys/firmware/beepy/led_blue', 'w') as blue:
            blue.write("128")
        if now - BUTTON_RELEASE_TIME > REPEAT_TIMEOUT:
            execute_script('short_press_1.sh')

def set_white_led():
    with open('/sys/firmware/beepy/led', 'w') as led:
        led.write('1')
    with open('/sys/firmware/beepy/led_red', 'w') as led:
        led.write('255')
    with open('/sys/firmware/beepy/led_green', 'w') as led:
        led.write('255')
    with open('/sys/firmware/beepy/led_blue', 'w') as led:
        led.write('255')

def turn_off_led():
    with open('/sys/firmware/beepy/led', 'w') as led:
        led.write('0')

def execute_script(script_name):
    global SHORT_PRESS_COUNT
    SHORT_PRESS_COUNT = 0

    script_path = os.path.join(os.path.expanduser('~/bin'), script_name)
    if os.path.exists(script_path):
        os.system(script_path)
    else:
        print(f'Create a script at {script_path} for this action')

    time.sleep(0.5)
    # Don't turn off the LED here

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=my_callback, bouncetime=50)  # 50ms for de-bouncing

    while True:
        handle_press()

except KeyboardInterrupt:
    print("Goodbye!")
finally:
    GPIO.cleanup()
