# Note: Requires root!
import wiringpi

PS_EN_PIN = 0  # Wiring Pi Pin = BCM GPIO 17 = Physical pin 11
DIM_PIN = 1  # Wiring Pi Pin = BCM GPIO 18 = Physical pin 12

MODE_GPIO = 1
MODE_PWM = 2

wiringpi.wiringPiSetup()
wiringpi.pinMode(PW_EN_PIN, wiringpi.OUTPUT)  # Physical pin 11, mode 1 = digital output maybe
wiringpi.pinMode(DIM_PIN, wiringpi.PWM_OUTPUT)  # Physical pin 12, mode 2 = PWM I guess
wiringpi.digitalWrite(PW_EN_PIN, 1)  # Turn on backlight

wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)  # Mark:space mode, not really sure
wiringpi.pwmSetClock(2)  # Range [2, 4095] maybe includes 1 also?
wiringpi.pwmSetRange(1024)  # [1, 4096] default=1024

# So
# This guy basically sets the duty cycle
# The value must be in the range of [0, max] where max is set by pwmSetRange
wiringpi.pwmWrite(1, 50)

# Frequency [Hz] = 19.2e6 / $clock / $range
# 19.2MHz is the processor speed
# $clock was set by pwmSetClock()
# $range was set by pwmSetRange()

# Helpful forum: https://raspberrypi.stackexchange.com/questions/4906/control-hardware-pwm-frequency
# What's going on?
# When you call pwmWrite(pin, $dc)
# The processor clock is ticking at 19.2MHz
# There is an internal counter register ($reg)
# For every $clock ticks, $reg is incremented
# if $reg < $dc: pin outputs HIGH
# if $reg >= $dc: pin outputs LOW
# if $reg > $range: $reg = 0

# Make sense?

# Example: You want to blink a thing at 1.45Hz because reasons
wiringpi.pwmSetClock(4095)
wiringpi.pwmSetRange(4095)
wiringpi.pwmWrite(1, 2048)  # 50% duty cycle (2048 / 4095)

