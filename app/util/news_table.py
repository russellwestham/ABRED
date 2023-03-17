import requests
import pandas as pd
from urllib.parse import urlparse
from config import settings

class NewsData():
    def __init__(self,search_word):
        self.client_id = settings.NEWS_CLIENT_ID
        self.client_secret = settings.NEWS_CLIENT_PW
        self.display_num = 100 # 1~100사이의 값
        self.url = 'https://openapi.naver.com/v1/search/news.json'
        self.search_word = search_word
        self.TOP_K = 10

    def get_data(self):
        headers = {'X-Naver-Client-Id':self.client_id, 'X-Naver-Client-Secret':self.client_secret}
        params = {'query':self.search_word, 'display':self.display_num, 'start':1, 'sort':'date'}
        response = requests.get(self.url, params = params, headers = headers)
        json = response.json()

        newslist = json['items']

        df = pd.DataFrame(newslist)
        if len(df) == 0 :
            return df
        # DB schema에 맞게 수정.
        df = df.drop('link', axis = 1) # 중복되는 link 삭제
        df = df.rename(columns = {'originallink' : 'url'}) #url로 바꿔주기
        df['thumnl_url'] = ''
        df['keywords'] = (df['title'] + ' ' + df['description']).str.replace('(&quot|<b>|</b>|&apos|;)','', regex= True)
        df['ks_graph'] = ''
        df = self.media_screening(df)
        return df

    def media_screening(self,df):
        media_list = [
            'www.yna.co.kr' #연합뉴스
            ,'www.hani.co.kr' #한겨레
            ,'news.kbs.co.kr' #KBS
            ,'www.chosun.com' #조선일보
            ,'www.khan.co.kr' #경향신문
            ,'www.hankookilbo.com' #한국일보
            ,'news.jtbc.co.kr' # JTBC
            ,'news.sbs.co.kr' # SBS
            ,'imnews.imbc.com' # MBC
            ,'www.joongang.co.kr' # 중앙일보
            ,'www.ytn.co.kr' # YTN
        ]       
        def parse_url(x):
            return urlparse(x).netloc
        df['media'] = df['url'].apply(parse_url)
        df = df[df['media'].isin(media_list)]
        return df
