from db import db
from sqlalchemy import Column, Integer, String

class Role(db.Model):

    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))

    def __init__(self, name):
        self.name = name