from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session
from config import settings
from model import create_tbl, ConstructionTable, Construction, NewsTable, News
import pandas as pd
# from deta import App
import news_table


app = FastAPI()

# TODO : define CORS policy 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------APIs------------
# @app.get("/users")
# async def read_users():
#     users = session.query(UserTable).all()
#     return users

# @app.get("/users/{user_id}")
# async def read_user(user_id: int):
#     user = session.query(UserTable).\
#         filter(UserTable.id == user_id).first()
#     return user

# @app.post("/user")
# async def create_user(name: str, age: int, email: str):
#     user = UserTable()
#     user.name = name
#     user.age = age
#     user.email = email
#     session.add(user)
#     session.commit()

# @app.put("/users")
# async def update_users(users: List[User]):
#     for new_user in users:
#         user = session.query(UserTable).\
#             filter(UserTable.id == new_user.id).first()
#         user.name = new_user.name
#         user.age = new_user.age
#         user.email = new_user.email
#         session.commit()

# # ----------test APIs------------
# @app.get("/target_items")
# async def read_target_items():
#     users = session.query(TargetItemTable).all()
#     return users
    
# @app.post("/target_item")
# async def create_target_item(name: str, keywords: str):
#     target_item = TargetItemTable()
#     target_item.name = name
#     target_item.keywords = keywords
#     session.add(target_item)
#     session.commit()


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
async def create_construction(name : str, type : str, stage : str, address : str, gis_data : str,):
    construction = ConstructionTable()
    construction.name = name
    construction.type = type
    construction.stage = stage
    construction.address = address
    construction.gis_data = gis_data
    #재개발 사업 별 keywords 구하기 
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
async def delete_construction(constructions: List[Construction],construction_id):
    construction = session.query(ConstructionTable).filter(ConstructionTable.id == construction_id).first()
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
@app.post("/news/{construction_name}")
# @app.post("/news")
async def create_news(construction_name : str):
    create_tbl()
    keyword = construction_name
    newsTable = news_table.NewsAPITable(keyword)
    df = newsTable.get_data()
    for i,row in df.iterrows(): 
        News = NewsTable()
        # construction id 찾기
        construction = session.query(ConstructionTable).filter(ConstructionTable.name == construction_name).first()
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
#news 새로고침 하기

