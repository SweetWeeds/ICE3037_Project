import threading
import time

from dynamixel_wrapper import MotorHandler
from db_manage import DB_Manager
from color_sensor import ColorSensor
from line_sensor import LineSensor
from ultra_sonic import UltraSonic

# Motor Settings
DEVICE_NAME     = '/dev/ttyUSB0'
LEFT_MOTOR_ID   = 1
RIGHT_MOTOR_ID  = 2
MOTOR_IDS       = [LEFT_MOTOR_ID, RIGHT_MOTOR_ID]
BAUDRATE        = 1000000

# Sensor Settings
LINE_SENSOR_PINS = []

# Constants
R = 0
G = 1
B = 2
STATUS = { 'STOP': 0, 'MOVING': 1, 'CHARGING': 2, 'COMPLETE': 3, 'EXCEPTION': 4 }
#POSITION = {'START': [0,0,0], 'A1': [R,G,R], 'A2': [R,G,B], 'A3': 3, 'A4': 4, 'B1', 'B2', 'B3', 'B4'}

class WC_Robo:
    def __init__(self) -> None:
        # Status
        self.status = STATUS['STOP']

        # DB Manager
        self.dbm = DB_Manager()

        # Init motors
        self.motorHandler = MotorHandler(DEVICE_NAME, MOTOR_IDS, BAUDRATE)
        self.__moveStop()
        self.__torqueEnable()

        # Sensors
        self.line_sensor = LineSensor(LINE_SENSOR_PINS)
        self.color_sensor = ColorSensor()
        self.ultra_sonic = UltraSonic()

        # Threads
        self.main_thread_inst = threading.Thread(group=self.__main_thread)
        self.db_listener_inst = threading.Thread(group=self.__db_listener_thread)

    ## Start of motor control Functions ##

    def __moveForward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, velocity)

    def __moveBackward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  -velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, -velocity)

    def __moveLeft(self) -> None:
        old_vel = self.motorHandler.setVelocityOffset(LEFT_MOTOR_ID,  20)
        time.sleep(0.5)
        self.motorHandler.setVelocity(LEFT_MOTOR_ID, old_vel)

    def __moveRight(self) -> None:
        old_vel = self.motorHandler.setVelocityOffset(RIGHT_MOTOR_ID, 20)
        time.sleep(0.5)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, old_vel)
    
    def __moveRotate(self, velocity: int = 100, clockwise: bool = True) -> None:
        if not clockwise:
            velocity = -velocity
        self.motorHandler.setVelocity(LEFT_MOTOR_ID, velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, -velocity)

    def __moveStop(self) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  0)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, 0)

    def __torqueDisable(self) -> None:
        self.motorHandler.setTorque(LEFT_MOTOR_ID,  False)
        self.motorHandler.setTorque(RIGHT_MOTOR_ID, False)

    def __torqueEnable(self) -> None:
        self.motorHandler.setTorque(LEFT_MOTOR_ID,  True)
        self.motorHandler.setTorque(RIGHT_MOTOR_ID, True)

    ## End of motor control Functions ##

    ## Control of charger ##
    def __startCharging(self):
        pass
    
    def __db_listener_thread(self):
        pass

    # Main thread
    def __main_thread(self):
        while(True):
            # Get Status Code
            if (self.status == STATUS['STOP']):
                continue    # IDLING
            elif (self.status == STATUS['MOVING']):
                pass
            elif (self.status == STATUS['CHARGING']):
                pass
            elif (self.status == STATUS['COMPLETE']):
                pass
            else:
                print(f"[ERROR] Status code is not matching in dictinoary. (STATUS_CODE:{self.status})")
                pass
    
    def run(self):
        self.main_thread_inst.start()
