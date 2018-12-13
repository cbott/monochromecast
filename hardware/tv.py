import RPi.GPIO as gpio

PS_ON_PIN = 11  # GPIO 17
DIM_PIN = 12  # GPIO 18 (PWM)

STARTUP_FREQ = 100  # Hz
STARTUP_DC = 99  # % Duty Cycle

class TV_Controller:
    def __init__(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(PS_ON_PIN, gpio.OUT)
        gpio.setup(DIM_PIN, gpio.OUT)
        self.pwm = gpio.PWM(DIM_PIN, STARTUP_FREQ)
        self.pwm.start(STARTUP_DC)
        self.set_brightness(1)
        self.enable_system()

    def __del__(self):
        self.disable_system()
        gpio.cleanup()

    def enable_system(self):
        gpio.output(PS_ON_PIN, gpio.HIGH)
        self.enabled = True

    def disable_system(self):
        gpio.output(PS_ON_PIN, gpio.LOW)
        self.enabled = False

    def set_frequency(self, freq):
        """Set the PWM frequency in Hz"""
        freq = max(0, freq)  # Cannot have negative frequency
        self.pwm.ChangeFrequency(freq)

    def set_brightness(self, brightness):
        """Set the brightness (0 to 100%)"""
        brightness = max(0, min(brightness, 100))
        # 100 = off, 0 = full on
        self.pwm.ChangeDutyCycle(100 - brightness)
