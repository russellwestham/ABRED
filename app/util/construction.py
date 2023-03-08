import xml.etree.ElementTree as ET
import pandas as pd

# xml_data
# parse the XML file
tree = ET.parse('xml_data.xml')
root = tree.getroot()

data = []

# create empty dataframe
df = pd.DataFrame(columns=['BSNS_PK','GU_NM','BJDON_NM','BTYP_NM','STEP_SE_NM','CAFE_NM','REPRSNT_JIBUN','PROGRS_STTUS','CAFE_STTUS'
,'ZONE_NM','ZONE_ADRES','ZONE_AR','TOTAR','CTY_PLAN_SPFC_NM','CTY_PLAN_SPCFC_NM','LAD_BLDLND_AR','LAD_ROAD_AR','LAD_PARK_AR','LAD_GREENS_AR'
,'LAD_PBSPCE_AR','LAD_SCHUL_AR','LAD_ETC_AR','BILDNG_PRPOS_NM','BILDNG_BDTLDR','BILDNG_FLRSPCER','BILDNG_HG','BILDNG_GROUND_FLOOR_CO'
,'BILDNG_UNDGRND_FLOOR_CO','SUM_BILDNG_CO','BILDNG_60_CO','BILDNG_60_85_CO','BILDNG_85_CO','BILDNG_RM','LOCIMG01','LOCIMG02','LOCIMG03'
],index = [0,1,2,3])

# iterate through each 'row' element and extract the data
for row in root.findall('./row'):    
    # print(row)
    i=0
    d = {}
    for col in df.columns:
        df[col].loc[i] = row.find(col).text
    # d['BSNS_PK'] = row.find('BSNS_PK').text
    # d['GU_NM'] = row.find('GU_NM').text
    # d['BJDON_NM'] = row.find('BJDON_NM').text
    # d['BTYP_NM'] = row.find('BTYP_NM').text
    # d['STEP_SE_NM'] = row.find('STEP_SE_NM').text
    # d['CAFE_NM'] = row.find('CAFE_NM').text
    # d['REPRSNT_JIBUN'] = row.find('REPRSNT_JIBUN').text
    # d['PROGRS_STTUS'] = row.find('PROGRS_STTUS').text
    # d['CAFE_STTUS'] = row.find('CAFE_STTUS').text
    # d['ZONE_NM'] = row.find('ZONE_NM').text
    # d['ZONE_ADRES'] = row.find('ZONE_ADRES').text
    # d['ZONE_AR'] = row.find('ZONE_AR').text
    # d['TOTAR'] = row.find('TOTAR').text
    # d['CTY_PLAN_SPFC_NM'] = row.find('CTY_PLAN_SPFC_NM').text
    # d['CTY_PLAN_SPCFC_NM'] = row.find('CTY_PLAN_SPCFC_NM').text
    # d['LAD_BLDLND_AR'] = row.find('LAD_BLDLND_AR').text
    # d['LAD_ROAD_AR'] = row.find('LAD_ROAD_AR').text
    # d['LAD_PARK_AR'] = row.find('LAD_PARK_AR').text
    # d['LAD_GREENS_AR'] = row.find('LAD_GREENS_AR').text
    # d['LAD_PBSPCE_AR'] = row.find('LAD_PBSPCE_AR').text
    # d['LAD_SCHUL_AR'] = row.find('LAD_SCHUL_AR').text
    # d['LAD_ETC_AR'] = row.find('LAD_ETC_AR').text
    # d['BILDNG_PRPOS_NM'] = row.find('BILDNG_PRPOS_NM').text
    # d['BILDNG_BDTLDR'] = row.find('BILDNG_BDTLDR').text
    # d['BILDNG_FLRSPCER'] = row.find('BILDNG_FLRSPCER').text
    # d['BILDNG_HG'] = row.find('BILDNG_HG').text
    # d['BILDNG_GROUND_FLOOR_CO'] = row.find('BILDNG_GROUND_FLOOR_CO').text
    # d['BILDNG_UNDGRND_FLOOR_CO'] = row.find('BILDNG_UNDGRND_FLOOR_CO').text
    # d['SUM_BILDNG_CO'] = row.find('SUM_BILDNG_CO').text
    # d['BILDNG_60_CO'] = row.find('BILDNG_60_CO').text
    # d['BILDNG_60_85_CO'] = row.find('BILDNG_60_85_CO').text
    # d['BILDNG_85_CO'] = row.find('BILDNG_85_CO').text
    # d['BILDNG_RM'] = row.find('BILDNG_RM').text
    # d['LOCIMG01'] = row.find('LOCIMG01').text
    # d['LOCIMG02'] = row.find('LOCIMG02').text
    # d['LOCIMG03'] = row.find('LOCIMG03').text
    # print(d)
    i+=1    
print(df)

# print dataframe
# print(df)
