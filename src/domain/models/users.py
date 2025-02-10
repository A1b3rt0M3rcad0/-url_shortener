from sqlalchemy import DateTime

class Users:
    def __init__(self, username:str, password:str, is_active:bool, created_at:DateTime):
        self.username = username
        self.password = password
        self.is_active = is_active
        self.created_at = created_at
        