import sys
import threading
import time
import RPi.GPIO as GPIO

sys.path.append("/home/pi/workspace/ICE3037_Project/WC-Robo/module")

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
SERVO_PIN = 13
LINE_SENSOR_PINS = [12,16,20,21]
ULTRASONIC_SENSOR_PINS = { "UP" : {
                                "Trig": 19,
                                "Echo": 26
                                },
                           "FRONT" : {
                                "Trig" : 5,
                                "Echo" : 6
                                }
                        }

# Constants
R = 0
G = 1
B = 2
STATUS = { 'STOP': 0, 'MOVING': 1, 'CHARGING': 2, 'COMPLETE': 3, 'EXCEPTION': 4 }
HANDLING_TIME = 0.5
#POSITION = {'START': [0,0,0], 'A1': [R,G,R], 'A2': [R,G,B], 'A3': 3, 'A4': 4, 'B1', 'B2', 'B3', 'B4'}

class WC_Robo:
    def __init__(self) -> None:
        # Set GPIO Mode
        GPIO.setmode(GPIO.BCM)
        
        # Status
        self.status = STATUS['STOP']

        # DB Manager
        self.dbm = DB_Manager()

        # Init motors
        self.motorHandler = MotorHandler(DEVICE_NAME, MOTOR_IDS, BAUDRATE)
        self.__moveStop()
        self.__torqueEnable()

        # Init Linear Servo
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.linear_servo = GPIO.PWM(SERVO_PIN, 50)

        # Sensors
        self.line_sensor = LineSensor(LINE_SENSOR_PINS)
        self.color_sensor = ColorSensor()
        self.ultra_sonic = UltraSonic(ULTRASONIC_SENSOR_PINS)

        # Threads
        #self.main_thread_inst = threading.Thread(group=self.__main_thread)
        #self.db_listener_inst = threading.Thread(group=self.__db_listener_thread)


    ## Start of motor control Functions ##
    def __moveForward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, velocity)

    def __moveBackward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  -velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, -velocity)

    def __moveLeft(self) -> None:
        old_vel = self.motorHandler.setVelocityOffset(LEFT_MOTOR_ID,  20)
        time.sleep(HANDLING_TIME)
        self.motorHandler.setVelocity(LEFT_MOTOR_ID, old_vel)

    def __moveRight(self) -> None:
        old_vel = self.motorHandler.setVelocityOffset(RIGHT_MOTOR_ID, 20)
        time.sleep(HANDLING_TIME)
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

    def sensorTest(self):
        while (True):
            print(f"line sensor: {self.line_sensor.read()}")
            print(f"color sensor: {self.color_sensor.read()}")
            print(f"ultra sonic: {self.ultra_sonic.reads()}")
            time.sleep(1)

    def motorTest(self):
        while (True):
            pass
    
    def servoTest(self):
        self.linear_servo.ChangeDutyCycle(12.5) #최댓값
        time.sleep(1)
        self.linear_servo.ChangeDutyCycle(10.0)
        time.sleep(1)
        self.linear_servo.ChangeDutyCycle(7.5) #0
        time.sleep(1)
        self.linear_servo.ChangeDutyCycle(5.0)
        time.sleep(1)
        self.linear_servo.ChangeDutyCycle(2.5) #최솟값
        time.sleep(1)
        self.linear_servo.stop()

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

    def __line_tracing_thread(self):
        while (True):
            sensor_tmp = self.line_sensor.read()
            

    def run(self):
        self.main_thread_inst.start()
