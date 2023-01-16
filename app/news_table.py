import requests
import pandas as pd

# import knowledge_graph as kg
# 기본적인 환경 설정
client_id = 'vBO9zHih5SAeoF0PnOOf'
client_secret = 'IdAZD84Gtl'
display_num = 10
url = 'https://openapi.naver.com/v1/search/news.json'


# 주어진 keyword 바탕으로 네이버 뉴스 api 이용해서 뉴스 데이터 수집 
keyword_list = '재개발'
headers = {'X-Naver-Client-Id':client_id, 'X-Naver-Client-Secret':client_secret}

params = {'query':keyword_list, 'display':display_num, 'start':1, 'sort':'date'}

response = requests.get(url, params = params, headers = headers)
integrated_document = ''
json = response.json()
newslist = json['items']


# dataframe 형태로 수집
df = pd.DataFrame(newslist)
# for i in range(len(df)):
#     print(df.iloc[i])

# db에 적재되는 형태랑 같도록 수정
df = df.drop('link', axis = 1) # 중복되는 link 삭제
df = df.rename(columns = {'originallink' : 'url'}) #url로 바꿔주기
df['thunl_url'] = ''
df['keywords'] = ''
df['ks_graph'] = ''
# # 하나의 문서로 통합하기
# for i in range(display_num):
#     if response.status_code == 200:
#         integrated_document += df['description'].iloc[i]
#         print(df['description'].iloc[i])
