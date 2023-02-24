import requests
import pandas as pd
from config import settings
from util.keyword_extractor import TextRankExtractor
                                # ,KeyBertExtractor, TFIDFExtractor, TopicRankExtractor, KeyBertEmbeddingExtractor
# import knowledge_graph as kg
# 기본적인 환경 설정
class NewsAPITable():
    def __init__(self,keyword):
        self.client_id = settings.NEWS_CLIENT_ID
        self.client_secret = settings.NEWS_CLIENT_PW
        self.display_num = 1
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

        # dataframe 형태로 수집
        df = pd.DataFrame(newslist)

        # db에 적재되는 형태랑 같도록 수정
        df = df.drop('link', axis = 1) # 중복되는 link 삭제
        df = df.rename(columns = {'originallink' : 'url'}) #url로 바꿔주기
        df['thumnl_url'] = ''
        # df['keywords'] = df['title'] + ' ' + df['description']
        # df['keywords'] = df['keywords'].apply(self.extract_keywords())
        df['ks_graph'] = ''
        return df


    def extract_keywords(self,df):
        df['keywords'] = (df['title'] + ' ' + df['description']).str.replace('(&quot|<b>|</b>|&apos|;)','', regex= True)
        docs = ''
        for i,row in df.iterrows():
            docs += row['keywords']
        df_docs = pd.DataFrame({'keywords' : [docs]})
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
            keyword_extractor = keyword_extractor_class(df_docs['keywords'], n_gram_range=(1,1))
            keywords = keyword_extractor.extract_keywords(top_n=self.TOP_K)

        return keywords['keywords'].iloc[0]
