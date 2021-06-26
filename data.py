import json
import sqlite3
import uuid
import success
import error
from info import info


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
        return "TEXT"
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


def get_default(p_type: str) -> str:
    if p_type.lower() == "uuid":
        return f"'{str(uuid.uuid1())}'"
    elif p_type.lower() == "string":
        return "'this is a null value'"
    elif p_type.lower() == "int":
        return "0"
    elif p_type.lower() == "double":
        return "0.0"
    elif p_type.lower() == "en-str":
        return "'this is a null value'"
    else:
        return "NULL"


def get_value(p_type: str, raw: str) -> str:
    if p_type.lower() == "uuid":
        return f"'{raw}'"
    elif p_type.lower() == "string":
        return f"'{raw}'"
    elif p_type.lower() == "int":
        return raw
    elif p_type.lower() == "double":
        return raw
    elif p_type.lower() == "en-str":
        return f"'{raw}'"
    else:
        return raw


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

        self.data = new_data

    def verification(self, db_name: str, table_name: str, parameter_names: list = None) -> bool:
        for db in self.data['db']:
            if str(db['db_name']).lower() == db_name.lower():
                for table in db['db_table']:
                    if str(table['table_name']).lower() == table_name.lower():
                        if parameter_names:
                            parameters = [str(x['parameter_name']).lower() for x in table['table_parameter']]
                            for p in parameter_names:
                                if str(p).lower() not in parameters:
                                    return False
                        return True
                return False
        return False

    def update(self, content: dict):
        if str(content['key']).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content['db_name'], content['table_name'], list(dict(content['new_data']).keys())):
            conn = sqlite3.connect(f"{content['db_name']}.db")
            c = conn.cursor()
            table_name = content['table_name'].upper()

            for u in content['new_data']:
                sql_command = f"UPDATE {table_name} set "
                sql_command += str(u).upper()
                sql_command += " = "
                sql_command += get_value(self.get_type(content['db_name'], content['table_name'], u),
                                         content['new_data'][u])
                sql_command += " where "
                sql_command += content['conditions'][u]

                c.execute(sql_command)

            conn.commit()
            conn.close()

            return success.Success("Update data successfully")
        else:
            return error.UpdateError('The database name or table name is incorrect')

    def insert(self, content: dict):
        if str(content['key']).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content['db_name'], content['table_name'], list(dict(content['insert_data']).keys())):
            conn = sqlite3.connect(f"{content['db_name']}.db")
            c = conn.cursor()
            table_name = content['table_name'].upper()
            sql_command = "INSERT " + "INTO " + table_name + " "
            p_info = "("
            p_value = " VALUES ("

            parameter_info = self.get_parameter_info(content['db_name'], content['table_name'])
            length = len(parameter_info)
            count = 0

            insert_keys = [str(x).upper() for x in dict(content['insert_data']).keys()]
            insert_data = [str(content['insert_data'][x]) for x in dict(content['insert_data'])]

            for p in parameter_info:
                p_info += p

                if p in insert_keys:
                    p_value += get_value(self.get_type(content['db_name'], content['table_name'], p),
                                         insert_data[insert_keys.index(str(p).upper())])
                else:
                    p_value += get_default(self.get_type(content['db_name'], content['table_name'], p))

                if count != (length - 1):
                    p_info += ", "
                    p_value += ", "

                count += 1

            p_info += ")"
            p_value += ")"

            sql_command = sql_command + p_info + p_value

            c.execute(sql_command)
            conn.commit()
            conn.close()

            return success.Success(f"Insert data successfully {p_value}")
        else:
            return error.InsertError('The database name or table name is incorrect')

    def delete(self, content: dict):
        if str(content['key']).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content['db_name'], content['table_name']):
            conn = sqlite3.connect(f"{content['db_name']}.db")
            c = conn.cursor()

            table_name = content['table_name'].upper()
            sql_command = "DELETE from "
            sql_command += f"{table_name} where "
            sql_command += content['condition']

            c.execute(sql_command)
            conn.commit()
            conn.close()

            return success.Success("Data deleted successfully")
        else:
            return error.InsertError('The database name or table name is incorrect')

    def get_parameter_info(self, db_name: str, table_name: str) -> list:
        res = []

        for db in self.data['db']:
            if str(db['db_name']).lower() == db_name.lower():
                for table in db['db_table']:
                    if str(table['table_name']).lower() == table_name.lower():
                        for p in table['table_parameter']:
                            res.append(str(p['parameter_name']).upper())

        return res

    def get_type(self, db_name: str, table_name: str, parameter_name: str) -> str:
        res = ""

        for db in self.data['db']:
            if str(db['db_name']).lower() == db_name.lower():
                for table in db['db_table']:
                    if str(table['table_name']).lower() == table_name.lower():
                        for p in table['table_parameter']:
                            if str(p['parameter_name']).lower() == parameter_name.lower():
                                res = p['parameter_type']
                                return res

        return res
