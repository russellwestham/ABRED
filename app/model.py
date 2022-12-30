# -*- coding: utf-8 -*-
# モデルの定義
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    age = Column(Integer)
    email = Column(String(50), nullable=False)


class User(BaseModel):
    id: int
    name: str
    age: int
    email: str


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
