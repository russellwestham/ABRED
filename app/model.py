# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List
from pydantic import BaseModel
from db import Base
from db import ENGINE


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
    avg_price_by_year = Column(JSON)

class ConstructionTable(Base):
    __tablename__ = 'Construction'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    news: Mapped[List["NewsTable"]] = relationship(
        back_populates="construction")  # 부모(construction)을 참조하는 참조변수(news)
    lots: Mapped[List["LotTable"]] = relationship(
        back_populates="construction")
    stats: Mapped[List["ConstructionStatTable"]] = relationship(
        back_populates="construction")
    preprice_simulations: Mapped[List["PrePriceSimulTable"]] = relationship(
        back_populates="construction")
    sale_informations: Mapped[List["SaleInfoTable"]] = relationship(
        back_populates="construction")
    gis_data = Column(String(50), nullable=False)
    keywords = Column(String(100), nullable=True)
    pyeong_cost = Column(Integer, nullable=False)
    donation_land_ratio = Column(Float, nullable=False)

    BSNS_PK = Column(String(50), nullable=False) #사업번호
    GU_NM = Column(String(30), nullable=False) #자치구 이름
    BJDON_NM = Column(String(30), nullable=False) #법정동
    BTYP_NM = Column(String(30), nullable=False) #사업구분
    STEP_SE_NM = Column(String(30), nullable=False) #운영구분
    CAFE_NM = Column(String(30), nullable=False) #추진위원회/조합명
    REPRSNT_JIBUN = Column(String(30), nullable=False) #대표지번
    PROGRS_STTUS = Column(String(30), nullable=False) #진행단계
    CAFE_STTUS = Column(String(30), nullable=False) #상태
    ZONE_NM = Column(String(30), nullable=False) #정비구역명칭
    ZONE_ADRES = Column(String(30), nullable=False) #정비구역위치
    ZONE_AR = Column(Float, nullable=False) #정비구역면적
    TOTAR = Column(Float, nullable=False) # 건축연면적
    CTY_PLAN_SPFC_NM = Column(String(50), nullable=False) # 용도지역
    CTY_PLAN_SPCFC_NM =  Column(String(30), nullable=False) #용도지구
    LAD_BLDLND_AR = Column(Float, nullable=True) #택지면적
    LAD_PBSPCE_AR = Column(Float, nullable=True) #공공면적
    LAD_ROAD_AR = Column(Float, nullable=True) # 도로면적
    LAD_PARK_AR = Column(Float, nullable=True) #공원면적
    LAD_GREENS_AR = Column(Float, nullable=True) #녹지면적
    LAD_SCHUL_AR = Column(Float, nullable=True) #학교면적
    LAD_ETC_AR = Column(Float, nullable=True) #기타면적
    BILDNG_PRPOS_NM = Column(String(30), nullable=False) #주용도
    BILDNG_BDTLDR  = Column(Float, nullable=False) # 건폐율
    BILDNG_FLRSPCER = Column(Float, nullable=False) # 용적률
    BILDNG_HG = Column(Float, nullable=False) # 높이
    BILDNG_GROUND_FLOOR_CO = Column(Integer, nullable=True) # 지상층수 
    BILDNG_UNDGRND_FLOOR_CO = Column(Integer, nullable=True) # 지하층수
    SUM_BILDNG_CO = Column(Integer, nullable=False) # 건설세대총수
    BILDNG_60_CO = Column(Integer, nullable=True) # 60미만 건설세대수
    BILDNG_60_85_CO = Column(Integer, nullable=True) # 60이상 85이하 건설세대수
    BILDNG_85_CO = Column(Integer, nullable=True) # 85초과 건설세대수
    BILDNG_RM =  Column(String(30), nullable=True) #건축계획비고
    LOCIMG01 = Column(String(50), nullable=False) #위치도
    LOCIMG02 = Column(String(50), nullable=False) #조감도
    LOCIMG03 = Column(String(50), nullable=False) #배치도


class Construction(BaseModel):
    id: int
    gis_data: str
    keywords: str
    pyeong_cost: int
    donation_land_ratio: float
    BSNS_PK : str #사업번호
    GU_NM : str #자치구 이름
    BJDON_NM : str #법정동
    BTYP_NM : str #사업구분
    STEP_SE_NM : str #운영구분
    CAFE_NM : str #추진위원회/조합명
    REPRSNT_JIBUN : str #대표지번
    PROGRS_STTUS : str #진행단계
    CAFE_STTUS : str #상태
    ZONE_NM : str #정비구역명칭
    ZONE_ADRES : str #정비구역위치
    ZONE_AR : float #정비구역면적
    TOTAR : float # 건축연면적
    CTY_PLAN_SPFC_NM : str # 용도지역
    CTY_PLAN_SPCFC_NM :  str #용도지구
    LAD_BLDLND_AR : float #택지면적
    LAD_PBSPCE_AR : float #공공면적
    LAD_ROAD_AR : float #도로면적
    LAD_PARK_AR : float #공원면적
    LAD_GREENS_AR : float #녹지면적
    LAD_SCHUL_AR : float #학교면적
    LAD_ETC_AR : float #기타면적
    BILDNG_PRPOS_NM : str #주용도
    BILDNG_BDTLDR  : float # 건폐율
    BILDNG_FLRSPCER : float # 용적률
    BILDNG_HG : float # 높이
    BILDNG_GROUND_FLOOR_CO : int # 지상층수 
    BILDNG_UNDGRND_FLOOR_CO : int # 지하층수
    SUM_BILDNG_CO : int # 건설세대총수
    BILDNG_60_CO : int # 60미만 건설세대수
    BILDNG_60_85_CO : int # 60이상 85이하 건설세대수
    BILDNG_85_CO : int # 85초과 건설세대수
    BILDNG_RM : str #건축계획비고
    LOCIMG01 : str #위치도
    LOCIMG02 : str #조감도
    LOCIMG03 : str #배치도


# News Table 설명
class NewsTable(Base):
    __tablename__ = 'News'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id: Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction: Mapped["ConstructionTable"] = relationship(back_populates="news")
    thumnl_url = Column(String(50), nullable=False)
    url = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    keywords = Column(String(50), nullable=True)
    ks_graph = Column(String(50), nullable=True)
    pubdate = Column(String(50), nullable=True)
    media = Column(String(50), nullable=True)
    


class News(BaseModel):
    id : int
    construction_id : int
    thumnl_url : str
    url : str
    title : str
    description : str
    pubdate : str
    keywords : str
    media :str
    # ks_graph = Column(String(50), nullable=True)


# Lot Price table
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



# PrePriceSimul talble
class PrePriceSimulTable(Base):
    __tablename__ = 'preprice_simulation'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id: Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction: Mapped["ConstructionTable"] = relationship(
        back_populates="preprice_simulations")
    pre_simul_date = Column(Integer, nullable=False)
    pre_predicted_prc = Column(Integer, nullable=False)
    building_number = Column(Integer, nullable=False)
    room_number = Column(Integer, nullable=False)
    
class PrePreiceSimul(BaseModel):
    id: int
    construction_id: int
    pre_simul_date: int
    pre_predicted_prc: int
    building_number: int
    room_number: int
    
# PostPriceSimul talble
class PostPriceSimulTable(Base):
    __tablename__ = 'postprice_simulation'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sale_information.id'), nullable=False)
    sale = relationship('SaleInfoTable', back_populates='postprices')
    post_simul_date = Column(Integer, nullable=False)
    post_predicted_prc = Column(Integer, nullable=False)

class PostPriceSimul(BaseModel):
    id: int
    construction_id: int
    #pyeong_type: int
    post_simul_date: int
    post_predicted_prc: int

# SaleInformation
class SaleInfoTable(Base):
    __tablename__ = 'sale_information'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    construction_id: Mapped[int] = mapped_column(ForeignKey("Construction.id"))
    construction: Mapped["ConstructionTable"] = relationship(
        back_populates="sale_informations")
    pyeong_type = Column(Integer, nullable=False)
    request_land = Column(Float, nullable=False)
    num_copartner_building = Column(Integer, nullable=False)
    num_general_building = Column(Integer, nullable=False)
    postprices = relationship('PostPriceSimulTable', back_populates='sale')

class SaleInfo(BaseModel):
    id: int
    construction_id: int
    pyeong_type: int
    request_land: float
    num_copartner_building: int
    num_general_building: int


def create_tbl():
    Base.metadata.create_all(bind=ENGINE)


def drop_tbl():
    Base.metadata.drop_all(bind=ENGINE)


if __name__ == "__main__":
    # for development only
    # drop_tbl()

    create_tbl()

    # for development only
    # from main import *
    # create_construction("test1", "test1", "test1", "test1", "test1")
