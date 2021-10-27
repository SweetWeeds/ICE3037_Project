from dynamixel_wrapper import MotorHandler
import threading

DEVICE_NAME     = '/dev/ttyUSB0'
LEFT_MOTOR_ID   = 1
RIGHT_MOTOR_ID  = 2
MOTOR_IDS       = [LEFT_MOTOR_ID, RIGHT_MOTOR_ID]
BAUDRATE        = 1000000

class WC_Robo:
    def __init__(self):
        self.motorHandler = MotorHandler(DEVICE_NAME, MOTOR_IDS, BAUDRATE)

    def setTarget(self, int):
        pass

    def move_forward(self, velocity: int):
        self.motorHandler.setVelocity(LEFT_MOTOR_ID, velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, velocity)

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_rotate(self, degree):
        pass

    def move_stop(self):
        self.motorHandler.setTorque(LEFT_MOTOR_ID, False)
        self.motorHandler.setTorque(RIGHT_MOTOR_ID, False)
    
    def start_Charging(self):
        pass

    def __callback_color_code(self):
        pass

    def start_SensorThread(self):
        pass