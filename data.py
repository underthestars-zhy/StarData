import json


class StarData:
    def __init__(self):
        new_data = None
        old_data = None
        with open("data.json") as f:
            if f.read() != "":
                new_data = json.load(f)
            else:
                return
        with open("config/data.json") as f:
            if f.read() != "":
                old_data = json.load(f)
            else:
                self.creat_db(new_data)

    def creat_db(self, db_data):
        
