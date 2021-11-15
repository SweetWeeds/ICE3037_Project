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
    
    def GetData(self, placeId):
        dir = db.reference(f"charge_request/{placeId}")
        return dir.get()
    
    def SetData(self, placeId, value):
        dir = db.reference(f"charge_request")
        dir.update({f"{placeId}":value})

    def _callback(self, e):
        #print(f"data:{e.data}, path:{e.path}, event_type:{e.event_type}")
        pass

    def startListen(self):
        dir = db.reference(f"charge_request")
        self.sess = dir.listen(self._callback)
