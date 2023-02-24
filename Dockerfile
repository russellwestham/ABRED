# python이라는 docker image를 받을건데, 그 버전은 3.11 버전으로 받겠다.
FROM python:3.11
# OS의 파일을 docker container안에 복사한다.
COPY requirements.txt .
# 믿을만한 host니깐, 파이썬 패키지들(pypi) 중에서 requirement.txt를 읽어서 안에 있는 것 설치
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# 파일 소유권에 대해서 host와 client의 daemon(default 값)을 mapping해서 복사하고, host의 app과 client의 /usr/src/app를 복사한다. 
COPY --chown=daemon:daemon ./app /usr/src/app
# ch(ange)mod(e) -R 파일들에 대해서 재귀적으로,  u(소유자)가 x(실행)할 수 있도록.
RUN chmod -R u+x /usr/src/app
# 마찬가지로 파일 복사
COPY alembic.ini /usr/src
# daemon이라는 user에 특정해서 명령  
USER daemon
# 이 디렉토리로 이동
WORKDIR /usr/src/app

RUN /bin/sh -c python -m nltk.downloader stopwords
RUN /bin/sh -c python -m nltk.downloader punkt
RUN /bin/sh -c python -m nltk.downloader averaged_perceptron_tagger

