import xml.etree.ElementTree as ET
from urllib.request import urlopen
import requests
import pandas as pd
from config import settings

class ConstructionData():
    def __init__(self):

        # 서울 열린데이터광장 - 서울시 부동산 실거래가 정보
        self.service_key = settings.CONSTRUCTION_SERVICE_KEY
        self.start_index = 1
        self.end_index = 1000
    def get_data(self):

        df_total = pd.DataFrame(columns=['BSNS_PK','GU_NM','BJDON_NM','BTYP_NM','STEP_SE_NM','CAFE_NM','REPRSNT_JIBUN','PROGRS_STTUS','CAFE_STTUS'
        ,'ZONE_NM','ZONE_ADRES','ZONE_AR','TOTAR','CTY_PLAN_SPFC_NM','CTY_PLAN_SPCFC_NM','LAD_BLDLND_AR','LAD_ROAD_AR','LAD_PARK_AR','LAD_GREENS_AR'
        ,'LAD_PBSPCE_AR','LAD_SCHUL_AR','LAD_ETC_AR','BILDNG_PRPOS_NM','BILDNG_BDTLDR','BILDNG_FLRSPCER','BILDNG_HG','BILDNG_GROUND_FLOOR_CO'
        ,'BILDNG_UNDGRND_FLOOR_CO','SUM_BILDNG_CO','BILDNG_60_CO','BILDNG_60_85_CO','BILDNG_85_CO','BILDNG_RM','LOCIMG01','LOCIMG02','LOCIMG03'
        ])

        GU_list = ['강남구','강동구','강북구','강서구','관악구','광진구','구로구','금천구','노원구','도봉구','동대문구','동작구','마포구','서대문구','서초구','성동구','성북구','송파구','양천구','영등포구','용산구','은평구','종로구','중구','중랑구']

        for GU_NM in GU_list:
            url = f"http://openAPI.seoul.go.kr:8088/{self.service_key}/xml/CleanupBussinessInfo/{self.start_index}/{self.end_index}/{GU_NM}"
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
        df_total = df_total.reset_index(drop = True)
        return df_total
