# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from pydantic import BaseModel
from db import Base
from db import ENGINE



# class UserTable(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(30), nullable=False)
#     age = Column(Integer)
#     email = Column(String(50), nullable=False)

# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#     email: str


# class TargetItemTable(Base):
#     __tablename__ = 'target_item'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(30), nullable=False)
#     keywords = Column(String(100), nullable=False)

# class TargetItem(BaseModel):
#     id: int
#     name: str
#     keywords: str

# Construction table 설명
class ConstructionTable(Base):
    __tablename__ = 'Construction'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    news : Mapped[List["NewsTable"]] = relationship(back_populates = "construction") #부모(construction)을 참조하는 참조변수(news)
    name = Column(String(30), nullable=False)
    type = Column(String(50), nullable=False)
    stage = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    gis_data = Column(String(50), nullable=False)
    keywords = Column(String(100), nullable=True)

class Construction(BaseModel):
    id : int
    name : str
    type : str
    stage : str
    address : str
    gis_data : str
    keywords : str

# News Table 설명
class NewsTable(Base):
    __tablename__ = 'News'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id : Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction : Mapped["ConstructionTable"] = relationship(back_populates = "news")

    thumnl_url = Column(String(50), nullable=False)
    url = Column(String(10000), nullable=False)
    title = Column(String(10000), nullable=False)
    description = Column(String(50000), nullable=False)
    # keywords = Column(String(50), nullable=True)
    ks_graph = Column(String(50), nullable=True)


class News(BaseModel):
    id = int
    construction_id = int
    thumnl_url = str
    url = str
    title = str
    description = str
    # keywords = str
    # ks_graph = Column(String(50), nullable=True)


def create_tbl():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    create_tbl()
