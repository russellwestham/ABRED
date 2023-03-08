import requests
import pandas as pd
from urllib.parse import urlparse
from config import settings
from util.keyword_extractor import TextRankExtractor
                                # ,KeyBertExtractor, TFIDFExtractor, TopicRankExtractor, KeyBertEmbeddingExtractor
# import knowledge_graph as kg
# 기본적인 환경 설정
class NewsAPITable():
    def __init__(self,keyword):
        self.client_id = settings.NEWS_CLIENT_ID
        self.client_secret = settings.NEWS_CLIENT_PW
        self.display_num = 100 # 1~100사이의 값
        self.url = 'https://openapi.naver.com/v1/search/news.json'
        self.keyword = keyword
        self.TOP_K = 10
    # 주어진 construction_id 바탕으로 네이버 뉴스 api 이용해서 뉴스 데이터 수집 
    def get_data(self):
        headers = {'X-Naver-Client-Id':self.client_id, 'X-Naver-Client-Secret':self.client_secret}
        params = {'query':self.keyword, 'display':self.display_num, 'start':1, 'sort':'date'}
        response = requests.get(self.url, params = params, headers = headers)
        json = response.json()

        newslist = json['items']

        df = pd.DataFrame(newslist)
        # 뉴스 데이터가 없는 경우 빈 df로 return
        if len(df) == 0 :
            return df
        # db에 적재되는 형태랑 같도록 수정
        df = df.drop('link', axis = 1) # 중복되는 link 삭제
        df = df.rename(columns = {'originallink' : 'url'}) #url로 바꿔주기
        df['thumnl_url'] = ''
        df['keywords'] = (df['title'] + ' ' + df['description']).str.replace('(&quot|<b>|</b>|&apos|;)','', regex= True)
        df['keywords'] = self.extract_keywords(df)
        df['ks_graph'] = ''
        df = self.media_screening(df)
        return df

    def merge_news(self, df):
        # 뉴스 데이터가 없는 경우 빈 df로 return
        if len(df) == 0 :
            return df
        # 뉴스 데이터가 있는 경우 
        docs = ''
        for i,row in df.iterrows():
            docs += row['keywords']
        df_docs = pd.DataFrame({'keywords' : [docs]})
        return df_docs

    def extract_keywords(self,df):
        # 뉴스 데이터가 없는 경우 빈 df로 return
        if len(df) ==0 :
            return df
        # 뉴스 데이터가 있는 경우
        keyword_extractors = {
        'text_rank' : TextRankExtractor,
        # 'tfidf' : TFIDFExtractor,
        # 'topic_rank' : TopicRankExtractor,
        # 'keybert' : KeyBertExtractor,
        }


        for keyword_extraction_method in [
        # 'tfidf',
        # 'keybert',
        'text_rank',
        # 'topic_rank'
        ]:
            keyword_extractor_class = keyword_extractors.get(keyword_extraction_method)
            keyword_extractor = keyword_extractor_class(df['keywords'], n_gram_range=(1,1))
            keywords = keyword_extractor.extract_keywords(top_n=self.TOP_K)

        return keywords['keywords']

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
