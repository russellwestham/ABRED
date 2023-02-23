from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session
from config import settings
from model import create_tbl, ConstructionTable, Construction, NewsTable, News, LotTable, Lot, ConstructionStatTable
import pandas as pd
# from deta import App
import util.news_table
from fastapi import HTTPException
from util.const_stats import update_stats

app = FastAPI()

# TODO : define CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------Constuction APIs------------
# 전체 construction 정보 가져오기
@app.get("/constructions")
async def read_constructions():
    constructions = session.query(ConstructionTable).all()
    return constructions
# 특정 construction 정보 가져오기


@app.get("/constructions/{construction_id}")
async def read_construction(construction_id: int):
    construction = session.query(ConstructionTable).\
        filter(ConstructionTable.id == construction_id).first()
    return construction
# 새로운 construction 추가하기


@app.post("/construction")
async def create_construction(name: str, type: str, stage: str, address: str, gis_data: str,):
    construction = ConstructionTable()
    construction.name = name
    construction.type = type
    construction.stage = stage
    construction.address = address
    construction.gis_data = gis_data
    # 재개발 사업 별 keywords 구하기
    newsTable = news_table.NewsAPITable(name)
    df = newsTable.get_data()
    construction.keywords = newsTable.extract_keywords(df)

    session.add(construction)
    session.commit()
# consturction 내용 변경하기


@app.put("/construction")
async def update_construction(constructions: List[Construction]):
    for new_construction in constructions:
        construction = session.query(ConstructionTable).\
            filter(ConstructionTable.id == new_construction.id).first()
        construction.name = new_construction.name
        construction.type = new_construction.type
        construction.stage = new_construction.stage
        construction.address = new_construction.address
        construction.gis_data = new_construction.gis_data
        construction.keywords = new_construction.keywords
        session.commit()
# construction 내용 삭제하기.


@app.delete("/construction/{construction_id}")
async def delete_construction(constructions: List[Construction], construction_id):
    construction = session.query(ConstructionTable).filter(
        ConstructionTable.id == construction_id).first()
    for new_construction in constructions:
        construction = session.query(ConstructionTable).\
            filter(ConstructionTable.id == new_construction.id).first()
        session.delete(construction)
        session.commit()


# ----------News APIs------------
# 전체 news 정보 가져오기
# @app.lib.run()
# @app.lib.cron()
# @app.put("/news_update")


@app.get("/news")
async def read_newses():
    news = session.query(NewsTable).all()
    return news
# # 특정 news 정보 가져오기


@app.get("/news/{news_id}")
async def read_news(news_id: int):
    news = session.query(NewsTable).\
        filter(NewsTable.id == news_id).first()
    return news
# # 새로운 news 추가하기


@app.post("/news/{construction_id}")
# @app.post("/news")
async def create_news(construction_id: str):
    create_tbl()
    keyword = construction_id
    newsTable = news_table.NewsAPITable(keyword)
    df = newsTable.get_data()
    for i, row in df.iterrows():
        News = NewsTable()
        # construction id 찾기
        construction = session.query(ConstructionTable).filter(
            ConstructionTable.id == construction_id).first()
        News.construction_id = construction.id
        # Newstable의 항목들 채우기
        News.thumnl_url = row['thumnl_url']
        News.url = row['url']
        News.title = row['title']
        News.description = row['description']
        # News.keywords = row['keywords']
        News.ks_graph = row['ks_graph']

        session.add(News)
        session.commit()
# # news 내용 변경하기


@app.put("/news")
async def update_news(newslist: List[News]):
    for new_news in newslist:
        news = session.query(NewsTable).\
            filter(NewsTable.id == new_news.id).first()
        news.const_id = new_news.const_id
        news.thumnl_url = new_news.thumnl_url
        news.url = new_news.url
        news.title = new_news.title
        news.description = new_news.description
        session.commit()
# # news 내용 삭제하기.


@app.delete("/news/{news_id}")
async def delete_news(newslist: List[News], news_id):
    news = session.query(NewsTable).\
        filter(NewsTable.id == news_id).first()
    for new_news in newslist:
        news = session.query(NewsTable).\
            filter(NewsTable.id == new_news.id).first()
        session.delete(news)
        session.commit()
# news 새로고침 하기


# ----------Lots APIs------------
# Lot CRUD APIs

@app.post("/lots")
async def create_lot(lot: Lot):
    db_lot = LotTable(
        construction_id=lot.construction_id,
        pnu=lot.pnu,
        coordinates=lot.coordinates,
        land_use_type=lot.land_use_type,
        land_area=lot.land_area,
        purpose_area_1=lot.purpose_area_1,
        purpose_area_2=lot.purpose_area_2,
        land_use_situation=lot.land_use_situation,
        topography_height=lot.topography_height,
        topography_form=lot.topography_form,
        road_side_type=lot.road_side_type
    )
    session.add(db_lot)
    session.commit()
    session.refresh(db_lot)
    return db_lot


@app.get("/lots/{lot_id}")
async def read_lot(lot_id: int):
    lot = session.query(LotTable).filter(LotTable.id == lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot


@app.put("/lots/{lot_id}")
async def update_lot(lot_id: int, lot: Lot):
    db_lot = session.query(LotTable).filter(LotTable.id == lot_id).first()
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    db_lot.construction_id = lot.construction_id
    db_lot.pnu = lot.pnu
    db_lot.coordinates = lot.coordinates
    db_lot.land_use_type = lot.land_use_type
    db_lot.land_area = lot.land_area
    db_lot.purpose_area_1 = lot.purpose_area_1
    db_lot.purpose_area_2 = lot.purpose_area_2
    db_lot.land_use_situation = lot.land_use_situation
    db_lot.topography_height = lot.topography_height
    db_lot.topography_form = lot.topography_form
    db_lot.road_side_type = lot.road_side_type
    session.commit()
    session.refresh(db_lot)
    return db_lot


@app.delete("/lots/{lot_id}")
async def delete_lot(lot_id: int):
    db_lot = session.query(LotTable).filter(LotTable.id == lot_id).first()
    if not db_lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    session.delete(db_lot)
    session.commit()
    return {"message": "Lot deleted successfully"}

# ----------Construction_stats APIs------------


@app.get("/construction_stats/{construction_id}")
async def read_construction_stat(construction_id: int):
    update_stats()

    construction_stat = session.query(ConstructionStatTable).\
        filter(ConstructionStatTable.construction_id == construction_id).first()
    return construction_stat
