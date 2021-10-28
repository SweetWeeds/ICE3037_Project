
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

# Device settings
DEVICE_NAME = '/dev/ttyUSB0'
PROTOCOL_VERSION = 2.0

# Address of parameters
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_VELOCITY = 104

# Constants
MIN_VELOCITY = -1023
MAX_VELOCITY = 1023


class MotorHandler:
    def __init__(self, DEVICE_NAME: str, IDs: list, BAUDRATE: int):
        self.portHandler = PortHandler(DEVICE_NAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)

        # Open port
        if self.portHandler.openPort():
            print(f"[INFO] Open the port({DEVICE_NAME})")
        else:
            print(f"[ERROR] Cannot open the port({DEVICE_NAME})")
            quit()

        # Set Baudrate
        if self.portHandler.setBaudRate(BAUDRATE):
            pass
        else:
            quit()

        # Get Motor IDs and set torque
        self.motors = dict()
        for idx, id in enumerate(self.IDs):
            self.motors.update({id : Motor(id, 0)})
            self.setTorque(id, True)

    def __error_check(self, dxl_comm_result, dxl_error):
        if dxl_comm_result != COMM_SUCCESS:
            print("[INFO] %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("[ERROR] %s" % self.packetHandler.getRxPacketError(dxl_error))

    def setTorque(self, ID: int, en: bool) -> None:
        if (en):
            en = 1
        else:
            en = 0
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, en)
        self.__error_check(dxl_comm_result, dxl_error)

    def setVelocity(self, ID: int, val: int) -> None:
        if (val < MIN_VELOCITY):
            val = MIN_VELOCITY
        if (val > MAX_VELOCITY):
            val = MAX_VELOCITY
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, ADDR_GOAL_VELOCITY, val)
        self.__error_check(dxl_comm_result, dxl_error)

    def readVelocity(self, ID: int) -> int:
        dxl_goal_vel, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, ID, ADDR_GOAL_VELOCITY)
        self.__error_check(dxl_comm_result, dxl_error)
        return dxl_goal_vel

    def setVelocityOffset(self, ID: int, val: int) -> int:
        old_vel = self.readVelocity(ID)
        self.setVelocity(ID, old_vel + val)
        return old_vel