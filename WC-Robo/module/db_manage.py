import pathlib
import firebase_admin
from firebase_admin import credentials, db

key_file = pathlib.Path("/home/pi/workspace/ICE3037_Project/Keys/qr-code-cd037-firebase-adminsdk-2hncv-5bef4fc373.json")

class DB_Manager:
    def __init__(self, key_file=key_file):
        config = {
            "databaseURL": "https://qr-code-cd037-default-rtdb.firebaseio.com/"
        }
        self.cred = credentials.Certificate(key_file)
        firebase_admin.initialize_app(self.cred, config)
        self.update_signal = False  # Update signal for data update check
        self.target_location = None

    def __GetData(self, reference, placeId):
        dir = db.reference(f"{reference}/{placeId}")
        return dir.get()
    
    def __SetData(self, reference: str, placeId: str, value: str) -> None:
        dir = db.reference(reference)
        dir.update({f"{placeId}":value})

    # Callback Function
    def __callback(self, e) -> None:
        print(f"data:{e.data}, path:{e.path}, event_type:{e.event_type}")

    # Start listening 
    def startListen(self) -> None:
        dir = db.reference(f"charge_request")
        self.sess = dir.listen(self.__callback)

    # Send charging status
    def sendChargeStatus(self, val: int) -> None:
        self.__SetData("charge_status", "wc-robo:1", str(val))

    # Set default location    
    def setDefaultLocation(self) -> None:
        self.__SetData("charge_request", "Home")

    def updateChargingStatus(self, reference, chargingStatus, chargePercentage, voltageValue):
        dir = db.reference(f"charge_status/{reference}")
        dir.update({"chargingStatus": chargingStatus, "chargePercentage": chargePercentage, "voltageValue": voltageValue})