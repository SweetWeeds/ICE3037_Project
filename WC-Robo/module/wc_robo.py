import sys
import threading
import time
import RPi.GPIO as GPIO
import PyBeacon

sys.path.append("/home/pi/workspace/ICE3037_Project/WC-Robo/module")

from dynamixel_wrapper import MotorHandler
from db_manage import DB_Manager
from color_sensor import ColorSensor
from line_sensor import LineSensor
from ultra_sonic import UltraSonic
from settings import *

class WC_Robo:
    def __init__(self) -> None:
        # Set GPIO Mode
        GPIO.setmode(GPIO.BCM)

        # Signal
        self.control_signal = CONTROL_SIGNAL['IDLE']

        # Status
        self.status = STATUS['STOP']
        self.line_sensor_val = list
        self.color_sensor_val = 'E'
        self.ultra_sonic_val = 0

        # DB Manager
        self.dbm = DB_Manager()

        # Init motors
        self.motorHandler = MotorHandler(DEVICE_NAME, MOTOR_IDS, BAUDRATE)
        self.__moveStop()
        self.__torqueEnable()

        # Init Linear Servo
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        self.linear_servo = GPIO.PWM(SERVO_PIN, 50)
        self.linear_servo_pos = 0
        self.linear_servo.start(0)
        self.__setServoPos(self.linear_servo_pos)

        # Sensors
        self.line_sensor = LineSensor(LINE_SENSOR_PINS)
        self.color_sensor = ColorSensor()
        self.ultra_sonic = UltraSonic(ULTRASONIC_SENSOR_PINS)

        # Threads
        self.main_thread_inst = threading.Thread(target=self.__main_thread)
        #self.db_listener_inst = threading.Thread(group=self.__db_listener_thread)

        self.line_trace_active = True  # Signal for line tracing
        self.line_tracing_thread_inst = threading.Thread(target=self.line_tracing_thread)

    def __read_sensors(self):
        self.line_sensor_val    = self.line_sensor.read()
        self.color_sensor_val   = self.color_sensor.read()
        self.ultra_sonic_val    = self.ultra_sonic.read()

    ## Start of motor control Functions ##
    ## DYNAMIXEL Control Code ##
    def __moveForward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, velocity)

    def __moveBackward(self, velocity: int = 100) -> None:
        self.motorHandler.setVelocity(LEFT_MOTOR_ID,  -velocity)
        self.motorHandler.setVelocity(RIGHT_MOTOR_ID, -velocity)

    def __moveLeft(self, val=20) -> None:
        old_vel = self.motorHandler.setVelocityOffset(LEFT_MOTOR_ID,  val)
        time.sleep(HANDLING_TIME)
        self.motorHandler.setVelocity(LEFT_MOTOR_ID, old_vel)

    def __moveRight(self, val=20) -> None:
        old_vel = self.motorHandler.setVelocityOffset(RIGHT_MOTOR_ID, val)
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
    ## End of DYNAMIXEL Control Code ##
    

    ## Linear Servo Code ##
    def __setServoPos(self, degree: float):
        if degree > 180.0:
            degree = 180.0
        if degree < 0.0:
            degree = 0.0
        duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
        print("Degree: {} to {}(Duty)".format(degree, duty))
        self.linear_servo.ChangeDutyCycle(duty)

    def __coilMoveDefault(self) -> None:
        self.__setServoPos(0.0)
        time.sleep(0.5)

    def __coilMoveUp(self, val: float=3.0) -> None:
        self.linear_servo_pos += val
        self.__setServoPos(self.linear_servo_pos)
        time.sleep(0.5)
        print(f"Current Coil Pos:{self.linear_servo_pos}")
    
    def __coilMoveDown(self, val: float=3.0) -> None:
        self.linear_servo_pos -= val
        self.__setServoPos(self.linear_servo_pos)
        time.sleep(0.5)
        print(f"Current Coil Pos:{self.linear_servo_pos}")
    ## End of Linear Servo Code ##

    ## End of motor control Functions ##


    ## Control of charger ##
    def __startCharging(self) -> None:
        pass

    def __db_listener_thread(self) -> None:
        self.dbm.startListen()

    ## Test Functions ##
    """
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
        self.linear_servo.start(0)
        self.linear_servo.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        self.linear_servo.ChangeDutyCycle(2)
        time.sleep(0.5)
        self.linear_servo.ChangeDutyCycle(3)
        time.sleep(0.5)
        self.linear_servo.ChangeDutyCycle(4)
        time.sleep(0.5)
        self.linear_servo.ChangeDutyCycle(5)
        time.sleep(0.5)
        self.linear_servo.ChangeDutyCycle(6)
        time.sleep(0.5)
    """
    ## End of test functions ##


    # Setup Coil
    def setCoil(self) -> None:
        print("[INFO] Start coil setup")
        while (True):
            currentDist = self.ultra_sonic.read("COIL")
            
            # Current Distance is closer than low bound limit: STOP
            if (currentDist < ULTRASONIC_BOUNDARY["COIL"]["LOWER_BOUND"]):
                print(f"Coil setup at {currentDist}")
                return None
            # Current Distance is 
            elif (currentDist >= ULTRASONIC_BOUNDARY["COIL"]["LOWER_BOUND"]):
                self.__coilMoveUp(10)
                pass
            else:
                pass
    
    # Setup Front
    def setFront(self) -> None:
        print("[INFO] Start front setup")
        self.__moveForward(10)
        while (True):
            currentDist = self.ultra_sonic.read("FRONT")
            print(f"currentDist:{currentDist}")
            if (currentDist < ULTRASONIC_BOUNDARY["FRONT"]["LOWER_BOUND"]):
                self.__moveStop()
                print(f"Forward setup at {currentDist}")
                return None
            else:
                continue

    def __moving(self):
        self.__read_sensors()   # Read sensor values

    # Main thread
    def __main_thread(self):
        while(True):
            # Get Status Code
            if (self.status == STATUS['STOP']):
                self.line_trace_active = False  # Deactivate line tracing
                self.__moveStop()               # Deactivate DYNAMIXEL
                continue    # IDLING
            elif (self.status == STATUS['MOVING']):
                self.line_trace_active = True   # Activate line tracing
                self.setFront()
                self.SetCoil()
                pass
            elif (self.status == STATUS['CHARGING']):
                self.line_trace_active = False  # Deactivate line tracing
                self.__moveStop()               # Deactivate DYNAMIXEL
                pass
            elif (self.status == STATUS['COMPLETE']):
                self.dbm.setDefaultLocation()   # Set target location into home and go back to home location.
            else:
                print(f"[ERROR] Status code is not matching in dictinoary. (STATUS_CODE:{self.status})")
                pass


    def line_tracing_thread(self):
        self.__moveForward()
        while (True):
            if (self.line_trace_active):
                line_sensor_tmp = self.line_sensor.read()
                # Turn Left (Strong)
                if line_sensor_tmp[0] and line_sensor_tmp[1] and not line_sensor_tmp[2] and not line_sensor_tmp[3]:
                    self.__moveLeft(20)
                elif not line_sensor_tmp[0] and line_sensor_tmp[1] and not line_sensor_tmp[2] and not line_sensor_tmp[3]:
                    self.__moveLeft(40)
                elif not line_sensor_tmp[0] and not line_sensor_tmp[1] and line_sensor_tmp[2] and line_sensor_tmp[3]:
                    self.__moveRight(20)
                elif not line_sensor_tmp[0] and not line_sensor_tmp[1] and line_sensor_tmp[2] and not line_sensor_tmp[3]:
                    self.__moveRight(40)
                else:
                    pass
            else:
                pass

    def run(self):
        self.main_thread_inst.start()
