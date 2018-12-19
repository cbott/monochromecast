# Note: Requires root!
import wiringpi

class TV_Controller:
    PW_EN_PIN = 0  # Wiring Pi # = BCM GPIO 17 = Physical pin 11
    DIM_PIN = 1  # Wiring Pi # = BCM GPIO 18 = Physical pin 12

    # HW PWM Attributes: See notes at end
    PWM_RANGE = 2048
    PWM_CLOCK = 64
    def __init__(self):
        wiringpi.wiringPiSetup()  # initialize wiringpi with default pin numbering
        wiringpi.pinMode(TV_Controller.PW_EN_PIN, wiringpi.OUTPUT)
        wiringpi.pinMode(TV_Controller.DIM_PIN, wiringpi.PWM_OUTPUT)

        wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS)  # Mark:space mode, unclear what this is
        wiringpi.pwmSetRange(TV_Controller.PWM_RANGE)
        wiringpi.pwmSetClock(TV_Controller.PWM_CLOCK)
        self.set_brightness(1)
        self.enable_system()

    def __del__(self):
        self.disable_system()
        # Set pins to input mode to disable output and set high impedance
        wiringpi.pinMode(TV_Controller.PW_EN_PIN, wiringpi.INPUT)
        wiringpi.pinMode(TV_Controller.DIM_PIN, wiringpi.INPUT)

    def enable_system(self):
        """ Send an enable signal to the power supply """
        wiringpi.digitalWrite(TV_Controller.PW_EN_PIN, True)
        self.enabled = True

    def disable_system(self):
        """ Stop sending enable signal to the power supply """
        wiringpi.digitalWrite(TV_Controller.PW_EN_PIN, False)
        self.enabled = False

    def set_brightness(self, brightness: float):
        """Set the brightness 0 to 100%"""
        brightness = max(0, min(brightness, 100))  # constrain inputs
        brightness *= brightness / 100  # square and renormalize

        min_command = 0
        max_command = TV_Controller.PWM_RANGE - 1  # For hardware reasons, PWM_RANGE - 1 is fully off

        command = max_command - (brightness / 100 * (max_command - min_command))
        # max_command = off, min_command = full on
        wiringpi.pwmWrite(TV_Controller.DIM_PIN, int(command))


# How hardware PWM works
# ----------------------
# Helpful forum: https://raspberrypi.stackexchange.com/questions/4906/control-hardware-pwm-frequency
# *
# PWM methods exposed by wiringpi
# ----------------------
# pwmSetClock(clock) # Based on testing $clock must fall in [3, 4095]
# pwmSetRange(range) # Based on testing $range must fall in [1, 4096]
# pwmWrite(pin, dc)  # pin must equal 1 (GPIO 18 for hardware PWM support)
#                    # dc must fall in the range [0, range]
# *
# Here is a pseudocode description of what's going on in hardware
# ```
# clock_register = 0
# output_register = 0
# def update_hardware_pwm():
#     clock_register += 1
#     if clock_register > clock:
#         output_register += 1
#         clock_register = 0

#     if output_register > range:
#         output_register = 0

#     if output_register < dc:
#         OUTPUT_HIGH_SIGNAL()
#     else:
#         OUTPUT_LOW_SIGNAL()
# ```
# Where the hardware calls the function update_hardware_pwm()
# At the processor frequency of 19.6MHz (19.2e6 times per second)
# *
# Therefore the resulting PWM frequency and duty cycle are
# freq [Hz] = 19.2e6 / clock / range
# duty_cycle = dc / range
# *
# The chosen value of range=2048, clock=64 gives us a frequency of
# 19.2e6 / 64 / 2048 = 146.48
# Which is above the frequency which a human can see flickering
