# python이라는 docker image를 받을건데, 그 버전은 3.11 버전으로 받겠다.
FROM python:3.11
# OS의 파일을 docker container안에 복사한다.

COPY alembic.ini /usr/src

WORKDIR /usr/src
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN ["chmod", "+x", "/wait-for-it.sh"]

RUN chmod -R u+x /usr/src

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

WORKDIR /usr/src/app

RUN /bin/sh -c python -m nltk.downloader stopwords
RUN /bin/sh -c python -m nltk.downloader punkt
RUN /bin/sh -c python -m nltk.downloader averaged_perceptron_tagger



