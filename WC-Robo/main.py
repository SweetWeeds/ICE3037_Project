import sys
from module.wc_robo import WC_Robo
import time

if __name__ == "__main__":
    wc_robo = WC_Robo()
    #wc_robo.coilMoveDefault()
    #wc_robo.run()
    #wc_robo.sensorTest()
    #wc_robo.coilMoveUp(3)
    #wc_robo.setFront()
    #wc_robo.setCoil()
    #wc_robo.line_tracing_thread()
    wc_robo.line_trace_active = True
    #wc_robo.line_tracing_thread()


