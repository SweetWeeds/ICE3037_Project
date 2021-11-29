import sys
from module.settings import *
from module.wc_robo import WC_Robo
import time

# Go to designated position
def goPos(wc_robo: WC_Robo, pos: str='A1'):
    if (pos not in LOCATION):
        print(f"[ERROR] There is no reserved position. [{pos}]")
        return
    wc_robo.dbm.updateChargingStatus(reference="wc-robo:1", chargingStatus="Moving", chargePercentage=f"0%")
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

    # 3. Set front position
    print("[INFO] Stage 3")
    initPos = wc_robo.readPresentPos()
    wc_robo.moveForward(10)
    while (True):
        dist = wc_robo.ultra_sonic.read("FRONT")
        if (dist <= ULTRASONIC_BOUNDARY["FRONT"]["LOWER_BOUND"]):
            break
    wc_robo.moveStop()
    return clockwise, initPos


def startCharge(wc_robo: WC_Robo) -> None:
    # Initialize Database status.
    wc_robo.dbm.updateChargingStatus(reference="wc-robo:1", chargingStatus="Charging", chargePercentage="")

    chargeRate = wc_robo.ble.recv()
    while (chargeRate != "100"):
        print(f"[INFO] Current Chargerate: {chargeRate}")
        wc_robo.dbm.updateChargingStatus(reference="wc-robo:1", chargingStatus="Charging", chargePercentage=f"{chargeRate}%")
        chargeRate = wc_robo.ble.recv()

    # Charging Complete
    wc_robo.dbm.updateChargingStatus(reference="wc-robo:1", chargingStatus="Complete", chargePercentage="100%")
    wc_robo.ble.close()

def main():
    wc_robo = WC_Robo()

    # Keep trying to connect with BLE
    while (wc_robo.ble.connect() == False):
        print("[INFO] Waiting for Bluetooth connection...")
        time.sleep(0.01) # Wait for 100ms

    while (True):
        # 1. Get session from database
        old_session = wc_robo.dbm.GetSession()
        while (True):
            new_session = wc_robo.dbm.GetSession()
            if (old_session != new_session):
                break

        # 2. Go to position
        clockwise, initPos = goPos(wc_robo, wc_robo.dbm.GetTargetPos())
        print(f"initPos:{initPos}")
        wc_robo.setCoil()
        startCharge(wc_robo)
        wc_robo.setServoPos(SERVO_MIN_POS)
        presentPos = wc_robo.readPresentPos()
        wc_robo.moveBackward(velocity=5)
        while (abs(presentPos[0] - initPos[0]) > 20 and abs(presentPos[1] - initPos[1]) > 20):
            presentPos = wc_robo.readPresentPos()
            print(f"presentPos{presentPos}")
        wc_robo.moveStop()

        # 3. Back to home
        wc_robo.moveRotate90(not clockwise)
        color = wc_robo.color_sensor.read()
        while (color != ROW['HOME']):
            wc_robo.line_trace_partial(forward=False)
            color = wc_robo.color_sensor.read()
            print(color)
        wc_robo.moveStop()
        print("[INFO] Request Complete!")

if __name__ == "__main__":
    main()
    wc_robo = WC_Robo()
    #wc_robo.moveStop()
    #while True:
    #    print(wc_robo.color_sensor.read())
