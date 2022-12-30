FROM python:3.11
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# RUN adduser --system --no-create-home fastapi
COPY --chown=daemon:daemon . /usr/src
RUN chmod -R u+x /usr/src/app
USER daemon
WORKDIR /usr/src/app
