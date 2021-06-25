import json
import sqlite3


def creat_db(db_data: dict):
    with open("config/data.json", 'w') as f:
        json.dump(db_data, f)

    for db in db_data["db"]:
        conn = sqlite3.connect(f'{db["db_name"]}.db')
        c = conn.cursor()

        for table in db["db_table"]:
            table_name = str(table["table_name"]).upper()
            sql_command = f"CREATE TABLE {table_name}\n"
            sql_command += "("

            length = len(table["table_parameter"])
            count = 0
            for p in list(table["table_parameter"]):
                command = f"{str(p['parameter_name']).upper()} {get_type(str(p['parameter_type']))}"
                if bool(p['is_primary']):
                    command += " PRIMARY KEY"
                if bool(p['not_null']):
                    command += "     NOT NULL"

                if count != (length - 1):
                    command += ",\n"

                sql_command += command
                count += 1

            sql_command += ");"

            c.execute(sql_command)

        conn.commit()
        conn.close()


def get_type(p_type: str) -> str:
    if p_type.lower() == "uuid":
        return "INTEGER"
    elif p_type.lower() == "string":
        return "NTEXT"
    elif p_type.lower() == "int":
        return "INTEGER"
    elif p_type.lower() == "double":
        return "DOUBLE"
    elif p_type.lower() == "en-str":
        return "TEXT"
    else:
        return "NULL"

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
