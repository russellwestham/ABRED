# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import settings


# def insertNewsData(session,df):
#     session.execute("daily news update")
#     df.to_sql(name = 'News', con = conn, if_exists = 'append', index = False)


ENGINE = create_engine(
    settings.DATABASE_URL,
    encoding="utf-8",
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)


Base = declarative_base()
Base.query = session.query_property()
