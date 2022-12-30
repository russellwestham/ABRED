FROM python:3.11
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY --chown=daemon:daemon ./app /usr/src/app
RUN chmod -R u+x /usr/src/app
COPY alembic.ini /usr/src

USER daemon
WORKDIR /usr/src/app
