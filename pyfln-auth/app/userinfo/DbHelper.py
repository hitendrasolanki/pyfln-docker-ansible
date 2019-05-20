from flask import current_app
from pymongo import MongoClient
import string

class DbHelper:
    def __init__(self):
        self.db_host = current_app.config['DATABASE_HOSTNAME']
        self.db_port = current_app.config['DATABASE_PORT']
        self.client = MongoClient(self.db_host,int(self.db_port.strip(string.ascii_letters)))
        self.db = self.client.test
        self.collection = self.db.registration