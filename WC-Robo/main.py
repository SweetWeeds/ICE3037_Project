import sys
from module.settings import *
from module.wc_robo import WC_Robo
import time

# Go to designated position
def goPos(wc_robo: WC_Robo, pos: str='A1') -> None:
    row = pos[0]    # 'A'
    col = pos[1]    # '1'
    # 1. Go to right row. ('A': 'R', 'B': 'B')
    print("[INFO] Stage 1")
    #wc_robo.line_tracing_thread_inst.start()
    while (wc_robo.color_sensor.read() != ROW[row]):
        wc_robo.line_trace_partial()
    #wc_robo.line_tracing_thread_inst.do_run = False
    wc_robo.moveStop()
    # 2. Rotate until find column line.
    print("[INFO] Stage 2")
    clockwise = True if col == '1' else False
    print(f"[INFO] Rotate :{clockwise}")
    wc_robo.moveRotate90(clockwise=clockwise)
    print("[INFO] Stage 3")

def startCharge(wc_robo: WC_Robo) -> None:
    wc_robo.ble.

if __name__ == "__main__":
    wc_robo = WC_Robo()
    """
    wc_robo.moveStop()
    while (True):
        cmd = input("Please type command: ")
        if (cmd == 'r'):
            wc_robo.moveRotate()
        elif (cmd == 's'):
            wc_robo.moveStop()
        elif (cmd == 'e'):
            print(wc_robo.readPresentPos())
    """
    goPos(wc_robo, 'B1')
    #wc_robo.moveRotate()
    #wc_robo.moveStop()

