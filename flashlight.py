import RPi.GPIO as GPIO
import time
import os

# GPIO pin for the button
BUTTON_PIN = 17

# Constants for timing
LONG_PRESS_DURATION = 2.0  # Time duration to detect a long press (2 seconds)

# LED state
led_on = False

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to handle a button press
def handle_press(channel):
    global button_held_start_time

    if GPIO.input(channel):  # Button released
        button_duration = time.time() - button_held_start_time

        if button_duration < LONG_PRESS_DURATION:  # Short press
            print("Short press detected")
            toggle_white_light()
    else:  # Button pressed
        button_held_start_time = time.time()

# Function to toggle the white light
def toggle_white_light():
    global led_on
    if led_on:
        print("Turning off the white light")
        turn_off_white_light()
    else:
        print("Turning on the white light")
        turn_on_white_light()

# Function to turn on the white light
def turn_on_white_light():
    global led_on
    with open('/sys/firmware/beepy/led', 'w') as led:
        led.write("0")  # Disable the LED
    with open('/sys/firmware/beepy/led_red', 'w') as red:
        red.write("255")  # Turn on red component
    with open('/sys/firmware/beepy/led_green', 'w') as green:
        green.write("255")  # Turn on green component
    with open('/sys/firmware/beepy/led_blue', 'w') as blue:
        blue.write("255")  # Turn on blue component
    with open('/sys/firmware/beepy/led', 'w') as led:
        led.write("1")  # Enable the LED
    led_on = True

# Function to turn off the white light
def turn_off_white_light():
    global led_on
    with open('/sys/firmware/beepy/led', 'w') as led:
        led.write("0")  # Disable the LED
    with open('/sys/firmware/beepy/led_red', 'w') as red:
        red.write("0")  # Turn off red component
    with open('/sys/firmware/beepy/led_green', 'w') as green:
        green.write("0")  # Turn off green component
    with open('/sys/firmware/beepy/led_blue', 'w') as blue:
        blue.write("0")  # Turn off blue component
    led_on = False

# Initialize variable
button_held_start_time = 0

# Add event detection for the button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=handle_press, bouncetime=50)

try:
    while True:
        time.sleep(1)  # Keep the script running

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
