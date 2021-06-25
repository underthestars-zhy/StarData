import json


def creat_db(db_data: dict):
    with open("config/data.json", 'w') as f:
        json.dump(db_data, f)


def get_json(file_path: str) -> dict:
    f = open(file_path)
    read = str(f.read())
    if read != "":
        result = dict(json.loads(read))
        f.close()
        return result
    else:
        f.close()
        return {}


class StarData:
    def __init__(self):
        new_data = get_json("./data.json")
        old_data = get_json("./config/data.json")

        if old_data == {}:
            creat_db(new_data)
