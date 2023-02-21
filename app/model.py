# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
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
class ConstructionStatTable(Base):
    __tablename__ = 'construction_stat'
    id = Column(Integer, primary_key=True, autoincrement=True)
    construction_id = Column(Integer, ForeignKey('Construction.id'))
    construction = relationship('ConstructionTable', back_populates='stats')
    avg_land_area = Column(Float, nullable=True)
    freq_purpose_area_1 = Column(JSON, nullable=True)
    freq_purpose_area_2 = Column(JSON, nullable=True)
    freq_land_use_situation = Column(JSON, nullable=True)
    freq_topography_height = Column(JSON, nullable=True)
    freq_topography_form = Column(JSON, nullable=True)
    freq_road_side_type = Column(JSON, nullable=True)
    cnt_lot = Column(Integer, nullable=True)


class ConstructionTable(Base):
    __tablename__ = 'Construction'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    news: Mapped[List["NewsTable"]] = relationship(
        back_populates="construction")  # 부모(construction)을 참조하는 참조변수(news)
    lots: Mapped[List["LotTable"]] = relationship(
        back_populates="construction")
    name = Column(String(30), nullable=False)
    type = Column(String(50), nullable=False)
    stage = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    gis_data = Column(String(50), nullable=False)
    keywords = Column(String(100), nullable=True)
    stats: Mapped[List[ConstructionStatTable]] = relationship(
        back_populates="construction")


class Construction(BaseModel):
    id: int
    name: str
    type: str
    stage: str
    address: str
    gis_data: str
    keywords: str

# News Table 설명


class NewsTable(Base):
    __tablename__ = 'News'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id: Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction: Mapped["ConstructionTable"] = relationship(
        back_populates="news")

    thumnl_url = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
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


class LotPriceTable(Base):
    __tablename__ = 'lot_price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lot_id = Column(Integer, ForeignKey('lot.id'), nullable=False)
    lot = relationship('LotTable', back_populates='prices')
    year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


class LotPrice(BaseModel):
    id: int
    lot_id: int
    year: int
    price: int


class LotTable(Base):
    __tablename__ = 'lot'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id: Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction: Mapped["ConstructionTable"] = relationship(
        back_populates="lots")
    pnu = Column(Integer, nullable=False)
    coordinates = Column(String(1024))
    land_use_type = Column(String(10))
    land_area = Column(Integer)
    purpose_area_1 = Column(String(30))
    purpose_area_2 = Column(String(30))
    land_use_situation = Column(String(10))
    topography_height = Column(String(10))
    topography_form = Column(String(10))
    road_side_type = Column(String(10))
    prices = relationship('LotPriceTable', back_populates='lot')


class Lot(BaseModel):
    id: int
    construction_id: int
    pnu: int
    coordinates: str
    land_use_type: str
    land_area: int
    purpose_area_1: str
    purpose_area_2: str
    land_use_situation: str
    topography_height: str
    topography_form: str
    road_side_type: str


def create_tbl():
    Base.metadata.create_all(bind=ENGINE)


def drop_tbl():
    Base.metadata.drop_all(bind=ENGINE)


if __name__ == "__main__":
    # for development only
    drop_tbl()
    create_tbl()

    # for development only
    # from main import *
    # create_construction("test1", "test1", "test1", "test1", "test1")
