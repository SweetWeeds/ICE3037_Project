import RPi.GPIO as GPIO
import time

class UltraSonic:
    def __init__(self, GPIO_PINs: dict) -> None:
        self.GPIO_PINs = GPIO_PINs
        for module, pins in self.GPIO_PINs.items():
            GPIO.setup(pins["Trig"], GPIO.OUT)
            GPIO.setup(pins["Echo"], GPIO.IN)

    # Return distance from module (metric: mm)
    def read(self, module):
        GPIO.output(self.GPIO_PINs[module]["Trig"], False)
        time.sleep(0.5)

        GPIO.output(self.GPIO_PINs[module]["Trig"], True)
        time.sleep(0.00001)
        GPIO.output(self.GPIO_PINs[module]["Trig"], False)

        while (GPIO.input(self.GPIO_PINs[module]["Echo"]) == 0):
            pulse_start = time.time()
        
        while (GPIO.input(self.GPIO_PINs[module]["Echo"]) == 1):
            pulse_end = time.time()
        
        pulse_dur = pulse_end - pulse_start
        dist = pulse_dur * 170000
        dist = round(dist, 2)

        return dist
    
    def reads(self):
        ret = dict()
        for key in self.GPIO_PINs.keys():
            val = self.read(key)
            ret.update({key : val})
        return ret