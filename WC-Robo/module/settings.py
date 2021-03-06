# Motor Settings
DEVICE_NAME     = '/dev/ttyUSB0'
LEFT_MOTOR_ID   = 1
RIGHT_MOTOR_ID  = 2
MOTOR_IDS       = [LEFT_MOTOR_ID, RIGHT_MOTOR_ID]
BAUDRATE        = 1000000

# Servo Settings
SERVO_MIN_POS     = 20
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기

# Sensor Settings
SERVO_PIN = 13
LINE_SENSOR_PINS = [12,16,20,21]    # Left to Right
ULTRASONIC_SENSOR_PINS ={
    "COIL" : {
        "Trig" : 19,
        "Echo" : 26
    },
    "FRONT" : {
        "Trig" : 5,
        "Echo" : 6
    }
}

ULTRASONIC_BOUNDARY = {
    "COIL" : {
        "LOWER_BOUND" : 30,
        "UPPER_BOUND" : 100
    }, 
    "FRONT" : {
        "LOWER_BOUND" : 35,
        "UPPER_BOUND" : 100
    }
}

# Constants
R = 0
G = 1
B = 2
ROW = { 'A': 'R', 'B': 'B', 'HOME': 'G' }    # Position row's dict
CONTROL_SIGNAL = { 'IDLE' : 0, 'GO_TARGET' : 1, 'SET_COIL' : 2, 'BACK_HOME' : 3 }
STATUS = { 'STOP': 0, 'MOVING': 1, 'CHARGING': 2, 'COMPLETE': 3, 'EXCEPTION': 4 }
HANDLING_TIME = 0.3
LOCATION = [ 'A1', 'A2', 'B1', 'B2' ]