import board
import adafruit_tcs34725

# Constants
R = 0
G = 1
B = 2
THRESHOLD = [35, 35, 50]    # RGB Threshold
Q_LEN = 10

class ColorSensor:
    def __init__(self) -> None:
        self.sensor = adafruit_tcs34725.TCS34725(board.I2C())
        self.r_q    = []
        self.g_q    = []
        self.b_q    = []
        self.rgb = [0, 0, 0]
    def read(self) -> str:
        #color_rgb_bytes_tmp = self.sensor.color_rgb_bytes
        self.rgb = self.sensor.color_rgb_bytes
        """
        self.r_q.append(color_rgb_bytes_tmp[R])
        if (len(self.r_q) > Q_LEN):
            self.r_q.pop(0)
        self.rgb[R] = sum(self.r_q, 0.0) / Q_LEN

        self.g_q.append(color_rgb_bytes_tmp[G])
        if (len(self.g_q) > Q_LEN):
            self.g_q.pop(0)
        self.rgb[G] = sum(self.g_q, 0.0) / Q_LEN

        self.b_q.append(color_rgb_bytes_tmp[B])
        if (len(self.b_q) > Q_LEN):
            self.b_q.pop(0)
        self.rgb[B] = sum(self.b_q, 0.0) / Q_LEN
        """
        print(self.rgb)
        color_rgb = [False, False, False]
        if (THRESHOLD[R] <= self.rgb[R]):
            color_rgb[R] = True
        if (THRESHOLD[G] <= self.rgb[G]):
            color_rgb[G] = True
        if (THRESHOLD[B] <= self.rgb[B]):
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