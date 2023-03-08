"""creation construction table and news table again

Revision ID: 3d2eb37bfcf4
Revises: 7b12567837d2
Create Date: 2023-01-17 08:12:15.268781

"""
from alembic import op
from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON,PrimaryKeyConstraint,ForeignKeyConstraint


# revision identifiers, used by Alembic.
revision = '3d2eb37bfcf4'
down_revision = '7b12567837d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'Construction'
        ,Column('id', Integer, nullable=False, index=True)
        ,Column('gis_data', String(50), nullable=False)
        ,Column('keywords', String(100), nullable=True)    
        ,Column('bsns_pk', String(50), nullable=False) #사업번호
        ,Column('GU_NM',String(30), nullable=False) #자치구 이름
        ,Column('BJDON_NM',String(30), nullable=False) #법정동
        ,Column('BTYP_NM',String(30), nullable=False) #사업구분
        ,Column('STEP_SE_NM',String(30), nullable=False) #운영구분
        ,Column('CAFE_NM',String(100), nullable=False) #추진위원회/조합명
        ,Column('REPRSNT_JIBUN',String(30), nullable=False) #대표지번
        ,Column('PROGRS_STTUS',String(30), nullable=False) #진행단계
        ,Column('CAFE_STTUS',String(30), nullable=False) #상태
        ,Column('ZONE_NM',String(100), nullable=True) #정비구역명칭
        ,Column('ZONE_ADRES',String(100), nullable=True) #정비구역위치
        ,Column('ZONE_AR',Float, nullable=True) #정비구역면적
        ,Column('TOTAR',Float, nullable=True) # 건축연면적
        ,Column('CTY_PLAN_SPFC_NM',String(200), nullable=True) # 용도지역
        ,Column('CTY_PLAN_SPCFC_NM',String(200), nullable=True) #용도지구
        ,Column('LAD_BLDLND_AR',Float, cnullable=True) #택지면적
        ,Column('LAD_PBSPCE_AR',Float, nullable=True) #공공면적
        ,Column('LAD_ROAD_AR',Float, nullable=True) # 도로면적
        ,Column('LAD_PARK_AR',Float, nullable=True) #공원면적
        ,Column('LAD_GREENS_AR',Float, nullable=True) #녹지면적
        ,Column('LAD_SCHUL_AR',Float, nullable=True) #학교면적
        ,Column('LAD_ETC_AR',Float, nullable=True) #기타면적
        ,Column('BILDNG_PRPOS_NM',String(100), nullable=True) #주용도
        ,Column('BILDNG_BDTLDR',Float, nullable=True) # 건폐율
        ,Column('BILDNG_FLRSPCER',Float, nullable=True) # 용적률
        ,Column('BILDNG_HG',Float, nullable=True) # 높이
        ,Column('BILDNG_GROUND_FLOOR_CO',Integer, nullable=True) # 지상층수 
        ,Column('BILDNG_UNDGRND_FLOOR_CO',Integer, nullable=True) # 지하층수
        ,Column('SUM_BILDNG_CO',Integer, nullable=False) # 건설세대총수
        ,Column('BILDNG_60_CO',Integer, nullable=True) # 60미만 건설세대수
        ,Column('BILDNG_60_85_CO',Integer, nullable=True) # 60이상 85이하 건설세대수
        ,Column('BILDNG_85_CO',Integer, nullable=True) # 85초과 건설세대수
        ,Column('BILDNG_RM',String(200), nullable=True) #건축계획비고
        ,Column('LOCIMG01',String(200), nullable=True) #위치도
        ,Column('LOCIMG02',String(200), nullable=True) #조감도
        ,Column('LOCIMG03',String(200), nullable=True) #배치도
        ,PrimaryKeyConstraint('id')
    )
    op.create_table(
    'News',
        Column('id', Integer, nullable=False, index=True),
        Column('construction_id', Integer, nullable=False, index=True),
        Column('thumnl_url', String(length=100), nullable=False),
        Column('url', String(length=100), nullable=False),
        Column('title', String(length=100), nullable=False),
        Column('description', String(length=500), nullable=False),
        Column('pubdate', String(length=50), nullable=False),
        Column('media', String(length=50), nullable=False),
        Column('ks_graph', String(length=100), nullable=False),
        PrimaryKeyConstraint('id'),
        ForeignKeyConstraint(['construction_id'], ['Construction.id'])
    )


def downgrade() -> None:
    op.drop_table('News')
    op.drop_table('Construction')
