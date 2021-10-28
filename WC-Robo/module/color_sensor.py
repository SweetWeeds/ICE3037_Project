import board
import adafruit_tcs34725

# Constants
R = 0
G = 1
B = 2
THRESHOLD = [50, 50, 50]    # RGB Threshold

class ColorSensor:
    def __init__(self) -> None:
        self.sensor = adafruit_tcs34725.TCS34725(board.I2C())

    def read(self) -> str:
        color_rgb_bytes_tmp = self.sensor.color_rgb_bytes
        color_rgb = [False, False, False]

        if (THRESHOLD[R] <= color_rgb_bytes_tmp[R]):
            color_rgb[R] = True
        if (THRESHOLD[G] <= color_rgb_bytes_tmp[G]):
            color_rgb[G] = True
        if (THRESHOLD[B] <= color_rgb_bytes_tmp[B]):
            color_rgb[B] = True

        # Get Color in string
        if (color_rgb[R] and not color_rgb[G] and not color_rgb[B]):
            return 'R'  # Red
        elif (not color_rgb[R] and color_rgb[G] and not color_rgb[B]):
            return 'G'  # Green
        elif (not color_rgb[R] and not color_rgb[G] and color_rgb[B]):
            return 'B'  # Blue
        elif (color_rgb[R] and color_rgb[G] and not color_rgb[B]):
            return 'Y'  # Red + Green = Yellow
        elif (color_rgb[R] and not color_rgb[G] and color_rgb[B]):
            return 'M'  # Red + Blue  = Magenta
        elif (not color_rgb[R] and color_rgb[G] and color_rgb[B]):
            return 'C'  # Green + Blue = Cyan
        elif (color_rgb[R] and color_rgb[G] and color_rgb[B]):
            return 'W'  # Red + Green + Blue = White
        elif (not color_rgb[R] and not color_rgb[G] and not color_rgb[B]):
            return 'D'  # None = Black(Dark)
        else:
            return 'E'  # Exception