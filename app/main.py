import pandas as pd
from fastapi import FastAPI,HTTPException
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session
from config import settings
from model import create_tbl, ConstructionTable, Construction, NewsTable, News, LotTable, Lot, ConstructionStatTable, PrePriceSimulTable, PrePriceSimul, PostPriceSimulTable, PostPriceSimul, SaleInfoTable, SaleInfo
from util.const_stats import update_stats
from util.keyword_extractor import get_news_keywords
import util.news_table as news_table


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


@app.get("/construction/{id}")
async def read_construction(id: int):
    construction = session.query(ConstructionTable).\
        filter(ConstructionTable.id == id).first()
    return construction

# 단일 새로운 construction 추가하기
@app.post("/construction")
async def create_construction(construction : Construction):
    db_construction = ConstructionTable(
        gis_data = construction.gis_data
        ,pyeong_cost = construction.pyeong_cost
        ,donation_land_ratio = construction.donation_land_ratio

        ,BSNS_PK = construction.BSNS_PK #사업번호
        ,GU_NM = construction.GU_NM #자치구 이름
        ,BJDON_NM = construction.BJDON_NM #법정동
        ,BTYP_NM = construction.BTYP_NM #사업구분
        ,STEP_SE_NM = construction.STEP_SE_NM #운영구분
        ,CAFE_NM = construction.CAFE_NM #추진위원회/조합명
        ,REPRSNT_JIBUN = construction.REPRSNT_JIBUN #대표지번
        ,PROGRS_STTUS = construction.PROGRS_STTUS #진행단계
        ,CAFE_STTUS = construction.CAFE_STTUS #상태
        ,ZONE_NM = construction.ZONE_NM #정비구역명칭
        ,ZONE_ADRES = construction.ZONE_ADRES #정비구역위치
        ,ZONE_AR = construction.ZONE_AR #정비구역면적
        ,TOTAR = construction.TOTAR # 건축연면적
        ,CTY_PLAN_SPFC_NM = construction.CTY_PLAN_SPFC_NM # 용도지역
        ,CTY_PLAN_SPCFC_NM = construction.CTY_PLAN_SPCFC_NM #용도지구
        ,LAD_BLDLND_AR = construction.LAD_BLDLND_AR #택지면적
        ,LAD_PBSPCE_AR = construction.LAD_PBSPCE_AR #공공면적
        ,LAD_ROAD_AR = construction.LAD_ROAD_AR # 도로면적
        ,LAD_PARK_AR = construction.LAD_PARK_AR #공원면적
        ,LAD_GREENS_AR = construction.LAD_GREENS_AR #녹지면적
        ,LAD_SCHUL_AR = construction.LAD_SCHUL_AR #학교면적
        ,LAD_ETC_AR = construction.LAD_ETC_AR #기타면적
        ,BILDNG_PRPOS_NM = construction.BILDNG_PRPOS_NM #주용도
        ,BILDNG_BDTLDR = construction.BILDNG_BDTLDR # 건폐율
        ,BILDNG_FLRSPCER = construction.BILDNG_FLRSPCER # 용적률
        ,BILDNG_HG =construction.BILDNG_HG # 높이
        ,BILDNG_GROUND_FLOOR_CO = construction.BILDNG_GROUND_FLOOR_CO # 지상층수 
        ,BILDNG_UNDGRND_FLOOR_CO = construction.BILDNG_UNDGRND_FLOOR_CO # 지하층수
        ,SUM_BILDNG_CO = construction.SUM_BILDNG_CO # 건설세대총수
        ,BILDNG_60_CO = construction.BILDNG_60_CO # 60미만 건설세대수
        ,BILDNG_60_85_CO = construction.BILDNG_60_85_CO # 60이상 85이하 건설세대수
        ,BILDNG_85_CO = construction.BILDNG_85_CO # 85초과 건설세대수
        ,BILDNG_RM = construction.BILDNG_RM #건축계획비고
        ,LOCIMG01 = construction.LOCIMG01 #위치도
        ,LOCIMG02 = construction.LOCIMG02 #조감도
        ,LOCIMG03 = construction.LOCIMG03 #배치도
    )
    session.add(db_construction)
    session.commit()
    session.refresh(db_construction)
    return db_construction



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


# @app.post("/news/{construction_id}")
# async def create_news_except_keywords(construction_id: str):
#     # construction id 찾기
#     construction = session.query(ConstructionTable).filter(ConstructionTable.id == construction_id).first()
#     table = news_table.NewsAPITable(construction.CAFE_NM)
#     df = table.get_data()
#     for i, row in df.iterrows():
#         db_News = NewsTable(
#         construction_id = construction.id
#         # Newstable의 항목들 채우기
#         ,thumnl_url = row['thumnl_url']
#         ,url = row['url']
#         ,title = row['title']
#         ,description = row['description']
#         ,keywords = row['keywords']
#         ,pubdate = row['pubDate']
#         ,ks_graph = row['ks_graph']
#         ,media = row['media']
#         ,keywords = ''
#         )
#         session.add(db_news)
#         session.commit()
#         session.refresh(db_news)
#         return db_news
# news의 키워드 업데이트
@app.post("/news/{construction_id}")
async def create_news_except_keywords(construction_id: str):
    # construction id 찾기
    construction = session.query(ConstructionTable).filter(ConstructionTable.id == construction_id).first()
    news_list = session.query(NewsTable).filter(NewsTable.id == construction_id).all()
    
    table = news_table.NewsAPITable(construction.CAFE_NM)
    df = table.get_data()
    for i, row in df.iterrows():
        db_News = NewsTable(
        construction_id = construction.id
        # Newstable의 항목들 채우기
        ,thumnl_url = row['thumnl_url']
        ,url = row['url']
        ,title = row['title']
        ,description = row['description']
        ,keywords = row['keywords']
        ,pubdate = row['pubDate']
        ,ks_graph = row['ks_graph']
        ,media = row['media']
        )
        session.add(db_news)
        session.commit()
        session.refresh(db_news)
        return db_news

# news 내용 변경하기
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
        news.pubdate = new_news.pubdate
        news.media = new_news.media
        session.commit()

# 뉴스 키워드 추가하기.
@app.put("/news/{construction_id}")
async def add_news_keywords(construction_id: str):
    # 뉴스가 속해있는 사업 데이터 가져오기
    construction = session.query(ConstructionTable).filter(ConstructionTable.id == construction_id).first()
    # 각 사업에 해당하는 뉴스들 가져오기
    news_list = session.query(NewsTable).filter(NewsTable.id == construction_id).all()
    # get_news_keywords를 사용하기 위한 준비 과정
    df_news = pd.DataFrame(columns = ['id','keywords'])
    for i in range(newslist):
        news_tbl = session.query(NewsTable).filter(NewsTable.id == news_list[i].id).first()
        df_news['id'].iloc[i] = news_tbl.id
        df_news['keywords'].iloc[i] = news_tbl.keywords
    # 각 뉴스별 키워드 추출
    df_news['keywords'] = get_news_keywords(df_news)
    # DB에 적제
    for i in range(newslist):
        news_tbl = session.query(NewsTable).filter(NewsTable.id == news_list[i].id).first()
        news_tbl.keywords = df_news['keywords'].iloc[i]
        session.add(news_tbl)
        session.commit()
        session.refresh(news_tbl)
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

# ----------preprice_simulation APIs------------
@app.get("/preprice_simulation/{construction_id}")
async def read_preprice_simulation(construction_id: int):
    preprice_simul = session.query(PrePriceSimulTable).\
        filter(PrePriceSimulTable.id == construction_id).first()
    return preprice_simul

@app.post("/preprice_simulation")
async def create_preprice_simulation(preprice: PrePriceSimul):
    db_preprice = PrePriceSimulTable(
        construction_id=preprice.construction_id,
        pre_simul_date=preprice.pre_simul_date,
        pre_predicted_prc=preprice.pre_predicted_prc,
        building_number=preprice.building_number,
        room_number=preprice.room_number
    )
    session.add(db_preprice)
    session.commit()
    session.refresh(db_preprice)
    return db_preprice

# ----------sale_information APIs------------
@app.get("/sale_information/{construction_id}")
async def read_preprice_simulation(construction_id: int):
    sale_information = session.query(SaleInfoTable).\
        filter(SaleInfoTable.id == construction_id).first()
    return sale_information

@app.post("/sale_information")
async def create_sale_information(saleinfo: SaleInfo):
    db_saleinfo = SaleInfoTable(
        construction_id=saleinfo.construction_id,
        pyeong_type=saleinfo.pyeong_type,
        request_land=saleinfo.request_land,
        num_copartner_building=saleinfo.num_copartner_building,
        num_general_building=saleinfo.num_general_building
    )
    session.add(db_saleinfo)
    session.commit()
    session.refresh(db_saleinfo)
    return db_saleinfo


# ----------postprice_simulation APIs------------
@app.get("/postprice_simulation/{construction_id}")
async def read_preprice_simulation(construction_id: int, sale_id: int):
    preprice = session.query(PostPriceSimulTable).\
        filter(PostPriceSimulTable.id == construction_id).first()
    return preprice

@app.post("/postprice_simulation")
async def create_sale_information(postprice: PostPriceSimul):
    db_postprice = PostPriceSimulTable(
        sale_id=postprice.sale_id,
        post_simul_date=postprice.post_simul_date,
        post_predicted_prc=postprice.post_predicted_prc
    )
    session.add(db_postprice)
    session.commit()
    session.refresh(db_postprice)
    return db_postprice
