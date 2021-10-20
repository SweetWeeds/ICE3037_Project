import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class DB_Manage:
    def __init__(self, key_file):
        self.cred = credentials.Certificate(key_file)
        firebase_admin.initialize_app(self.cred, {
            'databaseURL' : ''
        })