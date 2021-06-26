class Success:
    def __init__(self, message: str):
        self.type = "success"
        self.message = message


class Select:
    def __init__(self, message: str, values: list):
        self.type = "select"
        self.message = message
        self.value_dict = values
        self.value_list = []
        for x in values:
            res = []
            for i in x:
                res.append(x[i])
            self.value_list.append(res)
