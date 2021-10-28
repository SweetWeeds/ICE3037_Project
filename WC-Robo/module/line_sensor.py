import RPi.GPIO as GPIO

class LineSensor:
    def __init__(self, GPIO_PINs: list) -> None:
        # Initialize GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setmode(GPIO.BCM)

        self.GPIO_PINs = GPIO_PINs
        for p in self.GPIO_PINs:
            GPIO.setup(p, GPIO.IN)

    def read(self) -> list:
        ret = list()
        for p in self.GPIO_PINs:
            ret.append(GPIO.input(p))
        return ret
