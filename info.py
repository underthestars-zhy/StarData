from hashlib import md5


class Info:
    api_key = "ahdi1e3"
    private_key = "fhdiud1dj"
    salt = "star"

    def get_md5(self) -> str:
        md5_obj = md5()
        md5_obj.update(self.private_key + self.salt)
        return md5_obj.hexdigest()
