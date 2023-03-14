import os
import sys
import asyncio
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import requests
import pandas as pd
from config import settings
from model import ConstructionTable, Construction
from db import session
# import util.news_table as news_table
# from main import create_construction

# 서울 열린데이터광장 - 서울시 부동산 실거래가 정보

def get_data():
    service_key = os.getenv("CONSTRUCTION_SERVICE_KEY")
    start_index = 1
    end_index = 3
    # end_index = 1000
    # df 기본 구조
    df_total = pd.DataFrame(columns=['BSNS_PK','GU_NM','BJDON_NM','BTYP_NM','STEP_SE_NM','CAFE_NM','REPRSNT_JIBUN','PROGRS_STTUS','CAFE_STTUS'
    ,'ZONE_NM','ZONE_ADRES','ZONE_AR','TOTAR','CTY_PLAN_SPFC_NM','CTY_PLAN_SPCFC_NM','LAD_BLDLND_AR','LAD_ROAD_AR','LAD_PARK_AR','LAD_GREENS_AR'
    ,'LAD_PBSPCE_AR','LAD_SCHUL_AR','LAD_ETC_AR','BILDNG_PRPOS_NM','BILDNG_BDTLDR','BILDNG_FLRSPCER','BILDNG_HG','BILDNG_GROUND_FLOOR_CO'
    ,'BILDNG_UNDGRND_FLOOR_CO','SUM_BILDNG_CO','BILDNG_60_CO','BILDNG_60_85_CO','BILDNG_85_CO','BILDNG_RM','LOCIMG01','LOCIMG02','LOCIMG03'
    ])
    # 서울시 구 목록
    GU_list = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구','노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구','성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']
    # 각 구별로 api통해서 데이터 받아오기
    for GU_NM in GU_list:
        url = f"http://openAPI.seoul.go.kr:8088/{service_key}/xml/CleanupBussinessInfo/{start_index}/{end_index}/{GU_NM}"
        # url = f"http://openAPI.seoul.go.kr:8088/{service_key}/xml/CleanupBussinessInfo/{start_index}/{end_index}/{GU_NM}/{BJDON_NM}"

        content = requests.get(url).content
        root = ET.fromstring(content)

        # create empty dataframe
        df_gu = pd.DataFrame(columns=['BSNS_PK','GU_NM','BJDON_NM','BTYP_NM','STEP_SE_NM','CAFE_NM','REPRSNT_JIBUN','PROGRS_STTUS','CAFE_STTUS'
        ,'ZONE_NM','ZONE_ADRES','ZONE_AR','TOTAR','CTY_PLAN_SPFC_NM','CTY_PLAN_SPCFC_NM','LAD_BLDLND_AR','LAD_ROAD_AR','LAD_PARK_AR','LAD_GREENS_AR'
        ,'LAD_PBSPCE_AR','LAD_SCHUL_AR','LAD_ETC_AR','BILDNG_PRPOS_NM','BILDNG_BDTLDR','BILDNG_FLRSPCER','BILDNG_HG','BILDNG_GROUND_FLOOR_CO'
        ,'BILDNG_UNDGRND_FLOOR_CO','SUM_BILDNG_CO','BILDNG_60_CO','BILDNG_60_85_CO','BILDNG_85_CO','BILDNG_RM','LOCIMG01','LOCIMG02','LOCIMG03'
        ],index = range(len(root.findall('./row'))))
        i=0
        for row in root.findall('./row'):
            for col in df_gu.columns:
                df_gu[col].loc[i] = row.find(col).text
            i+=1
        df_total = pd.concat([df_total,df_gu], axis = 0)
        df_total['keywords'] = ''
    df_total = df_total.reset_index(drop = True)
    return df_total
def update_JeongBiSaeop_data(df_total):
    # def get_keywords(CAFE_NM):
    #     # 재개발 사업 별 keywords 구하기
    #     newsTable = news_table.NewsAPITable(CAFE_NM)
    #     df_news = newsTable.get_data()
    #     df_docs = newsTable.merge_news(df_news)
    #     if len(df_docs) !=0:
    #         keywords = newsTable.extract_keywords(df_docs).iloc[0]
    #     else :
    #         keywords = ''
    #     return keywords

    construction_list = []
    # df에서 각 row별로 construction 별로 뽑아내기
    for i, row in df_total.iterrows():
        construction = Construction(
            # id = i
            gis_data = ''
            ,pyeong_cost = 0
            ,donation_land_ratio = 0.0
            ,keywords = ''
            # 크롤링으로 가져온 데이터 넣기 
            ,BSNS_PK = row['BSNS_PK'] #사업번호
            ,GU_NM = row['GU_NM']#자치구 이름
            ,BJDON_NM = row['BJDON_NM']#법정동
            ,BTYP_NM = row['BTYP_NM']#사업구분
            ,STEP_SE_NM = row['STEP_SE_NM']#운영구분
            ,CAFE_NM = row['CAFE_NM'] #추진위원회/조합명
            ,REPRSNT_JIBUN = row['REPRSNT_JIBUN'] #대표지번
            ,PROGRS_STTUS = row['PROGRS_STTUS']#진행단계
            ,CAFE_STTUS = row['CAFE_STTUS'] #상태
            ,ZONE_NM = row['ZONE_NM'] #정비구역명칭
            ,ZONE_ADRES = row['ZONE_ADRES'] #정비구역위치
            ,ZONE_AR = row['ZONE_AR'] #정비구역면적
            ,TOTAR = row['TOTAR'] # 건축연면적
            ,CTY_PLAN_SPFC_NM = row['CTY_PLAN_SPFC_NM'] # 용도지역
            ,CTY_PLAN_SPCFC_NM = row['CTY_PLAN_SPCFC_NM']  #용도지구
            ,LAD_BLDLND_AR = row['LAD_BLDLND_AR'] #택지면적
            ,LAD_PBSPCE_AR = row['LAD_PBSPCE_AR'] #공공면적
            ,LAD_ROAD_AR = row['LAD_ROAD_AR'] # 도로면적
            ,LAD_PARK_AR = row['LAD_PARK_AR'] #공원면적
            ,LAD_GREENS_AR = row['LAD_GREENS_AR'] #녹지면적
            ,LAD_SCHUL_AR = row['LAD_SCHUL_AR'] #학교면적
            ,LAD_ETC_AR = row['LAD_ETC_AR'] #기타면적
            ,BILDNG_PRPOS_NM = row['BILDNG_PRPOS_NM'] #주용도
            ,BILDNG_BDTLDR  = row['BILDNG_BDTLDR'] # 건폐율
            ,BILDNG_FLRSPCER = row['BILDNG_FLRSPCER'] # 용적률
            ,BILDNG_HG = row['BILDNG_HG'] # 높이
            ,BILDNG_GROUND_FLOOR_CO = row['BILDNG_GROUND_FLOOR_CO'] # 지상층수 
            ,BILDNG_UNDGRND_FLOOR_CO = row['BILDNG_UNDGRND_FLOOR_CO'] # 지하층수
            ,SUM_BILDNG_CO = row['SUM_BILDNG_CO'] # 건설세대총수
            ,BILDNG_60_CO = row['BILDNG_60_CO'] # 60미만 건설세대수
            ,BILDNG_60_85_CO = row['BILDNG_60_85_CO'] # 60이상 85이하 건설세대수
            ,BILDNG_85_CO = row['BILDNG_85_CO'] # 85초과 건설세대수
            ,BILDNG_RM =  row['BILDNG_RM'] #건축계획비고
            ,LOCIMG01 = row['LOCIMG01'] #위치도
            ,LOCIMG02 = row['LOCIMG02'] #조감도
            ,LOCIMG03 = row['LOCIMG03'] #배치도
        )
        construction_list.append(construction)
    return construction_list

def store_in_db():
    df_total = get_data()
    construction_list = update_JeongBiSaeop_data(df_total)
    for construction in construction_list:
        db_construction = ConstructionTable(
            gis_data = construction.gis_data
            ,pyeong_cost = construction.pyeong_cost
            ,donation_land_ratio = construction.donation_land_ratio
            ,keywords = construction.keywords
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
        # construction_creation = create_construction(construction)
        # asyncio.run(construction_creation)
if __name__ == '__main__':
    store_in_db()
