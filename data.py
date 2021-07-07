import json
import sqlite3
import uuid
import success
import error
import schemas
from info import info
import os
from os.path import exists


def creat_db(db_data: dict, db_name: str = None):
    if not db_name:
        with open("./data/config/config.json", 'w') as f:
            json.dump(db_data, f)

        if not exists("data"):
            os.mkdir("data")

    for db in db_data["db"]:
        if not db_name:
            if not db['public']:
                continue
        else:
            if db['public']:
                continue
            if str(db['db_name']).lower() != db_name.lower().split("-")[0]:
                continue

        name = db["db_name"]
        if db_name:
            name = db_name

        conn = sqlite3.connect(f'data/db/{name}.db')
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
    elif p_type.lower() == "context":
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
    elif p_type.lower() == "context":
        return "'nil'"
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
    elif p_type.lower() == "context":
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
        new_data = get_json("config.json")
        old_data = get_json("./data/config/config.json")

        if old_data == {}:
            creat_db(new_data)

        self.data = new_data

    def verification(self, db_name: str, table_name: str = None, parameter_names: list = None) -> bool:
        for db in self.data['db']:
            if str(db['db_name']).lower().split("-")[0] == db_name.lower():
                if table_name:
                    for table in db['db_table']:
                        if str(table['table_name']).lower() == table_name.lower():
                            if parameter_names:
                                parameters = [str(x['parameter_name']).lower() for x in table['table_parameter']]
                                for p in parameter_names:
                                    if str(p).lower() not in parameters:
                                        return False
                            return True
                    return False
                return True
        return False

    def easy_get(self, api: str, db_name: str, table_name: str, name: str, value):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if self.verification(db_name, table_name):
            conn = sqlite3.connect(f"data/db/{db_name}.db")
            c = conn.cursor()
            table_name = table_name.upper()
            p = self.get_primary(db_name, table_name)

            sql_command = f"SELECT {name.upper()}"
            sql_command += f" from {table_name}"
            sql_command += f" where {p[0].upper()}={get_value(p[1], value)}"

            res = c.execute(sql_command)

            v = None
            for row in res:
                v = row[0]

            conn.close()

            return success.EasyGet(v)
        else:
            return error.UpdateError('The data name or table name is incorrect')

    def get_all_items(self, api: str, db_name: str, table_name: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if self.verification(db_name, table_name):
            conn = sqlite3.connect(f"data/db/{db_name}.db")
            c = conn.cursor()
            table_name = table_name.upper()

            sql_command = f"SELECT *"
            sql_command += f" from {table_name}"

            cursor = c.execute(sql_command)
            res = []
            parameters = self.get_parameter_info(db_name, table_name)

            for row in cursor:
                table = {}
                count = 0
                for p in parameters:
                    table[p] = row[count]
                    count += 1
                res.append(table)

            return success.EasyGet(res)
        else:
            return error.UpdateError('The data name or table name is incorrect')

    def creat_db(self, api: str, db_name: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if self.verification(db_name):
            context = str(uuid.uuid1())
            creat_db(self.data, f"{db_name}-{context}")

            return success.Context(context)
        else:
            return error.CreatDBError('The data name or table name is incorrect')

    def easy_verification(self, api: str, private_key: str, salt: str, db_name: str):
        if api == info.api_key and info.private_key == private_key and info.salt == salt and self.verification(db_name):
            return success.EasyVerification(True)
        else:
            return success.EasyVerification(False)

    def update(self, content: schemas.UpdateItem, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if str(content.key).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        all_parameter = []
        for i in content.new_data:
            for x in content.new_data[i]:
                all_parameter.append(x)

        if self.verification(content.db_name, content.table_name, all_parameter):
            conn = sqlite3.connect(f"data/db/{content.db_name}.db")
            c = conn.cursor()
            table_name = content.table_name.upper()

            for u in content.new_data:
                sql_command = f"UPDATE {table_name} set "
                count = 0
                length = len(content.new_data[u])

                for p in content.new_data[u]:
                    sql_command += str(p).upper()
                    sql_command += " = "
                    sql_command += get_value(self.get_type(content.db_name, content.table_name, p),
                                             content.new_data[u][p])

                    if count != (length - 1):
                        sql_command += ", "

                    count += 1

                sql_command += " where "
                sql_command += content.conditions[u]

                c.execute(sql_command)

            conn.commit()
            conn.close()

            return success.Success("Update data successfully")
        else:
            return error.UpdateError('The data name or table name is incorrect')

    def easy_set(self, content: schemas.EasySet, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if str(content.key).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content.db_name, content.table_name, [content.name]):
            conn = sqlite3.connect(f"data/db/{content.db_name}.db")
            c = conn.cursor()
            table_name = content.table_name.upper()
            p = self.get_primary(content.db_name, content.table_name)

            sql_command = f"UPDATE {table_name} set " + content.name.upper() + " = " + \
                          get_value(self.get_type(content.db_name, content.table_name, content.name), content.value) + \
                          f"where {p[0]}={get_value(p[1], content.primary)}"

            c.execute(sql_command)
            conn.commit()
            conn.close()
            return success.Success("Update data successfully")
        else:
            return error.InsertError('The data name or table name is incorrect')

    def insert(self, content: schemas.InsertItem, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if str(content.key).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content.db_name, content.table_name, list(content.insert_data.keys())):
            conn = sqlite3.connect(f"data/db/{content.db_name}.db")
            c = conn.cursor()
            table_name = content.table_name.upper()

            sql_command = "INSERT " + "INTO " + table_name + " "
            p_info = "("
            p_value = " VALUES ("

            parameter_info = self.get_parameter_info(content.db_name, content.table_name)
            length = len(parameter_info)
            count = 0

            insert_keys = [str(x).upper() for x in dict(content.insert_data).keys()]
            insert_data = [str(content.insert_data[x]) for x in dict(content.insert_data)]

            for p in parameter_info:
                p_info += p

                if p in insert_keys:
                    p_value += get_value(self.get_type(content.db_name, content.table_name, p),
                                         insert_data[insert_keys.index(str(p).upper())])
                else:
                    p_value += get_default(self.get_type(content.db_name, content.table_name, p))

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
            return error.InsertError('The data name or table name is incorrect')

    def delete(self, content: schemas.DeleteItem, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if str(content.key).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content.db_name, content.table_name):
            conn = sqlite3.connect(f"data/db/{content.db_name}.db")
            c = conn.cursor()

            table_name = content.table_name.upper()
            sql_command = "DELETE from "
            sql_command += f"{table_name} where "
            sql_command += content.condition

            c.execute(sql_command)
            conn.commit()
            conn.close()

            return success.Success("Data deleted successfully")
        else:
            return error.InsertError('The data name or table name is incorrect')

    def select(self, content: schemas.SelectItem, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        if str(content.key).lower() != info.get_md5():
            return error.ValidationError('The key is wrong, please check the salt and key')

        if self.verification(content.db_name, content.table_name):
            conn = sqlite3.connect(f"data/db/{content.db_name}.db")
            c = conn.cursor()
            table_name = content.table_name.upper()

            sql_command = "SELECT "
            count = 0
            length = len(content.select_parameter)

            for p in content.select_parameter:
                sql_command += p

                if count != (length - 1):
                    sql_command += ", "

                count += 1

            sql_command += " from "
            sql_command += table_name
            if content.other:
                sql_command += ' '
                sql_command += content.other
            print(sql_command)

            cursor = c.execute(sql_command)

            values = []
            for row in cursor:
                _c = 0
                res = {}
                for p in content.select_parameter:
                    res[p] = row[_c]
                values.append(res)

            conn.close()

            return success.Select("Successful search", values)
        else:
            return error.InsertError('The data name or table name is incorrect')

    def get_data_info(self, api: str):
        if api != info.api_key:
            return error.ValidationError('Unable to verify API key')

        return self.data

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

    def get_primary(self, db_name: str, table_name: str) -> [str, str]:
        res = ["", ""]

        for db in self.data['db']:
            if str(db['db_name']).lower() == db_name.lower():
                for table in db['db_table']:
                    if str(table['table_name']).lower() == table_name.lower():
                        for p in table['table_parameter']:
                            if bool(p['is_primary']):
                                res[0] = p['parameter_name']
                                res[1] = p['parameter_type']
                                return res
        return res
