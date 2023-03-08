# ABRED
 AI-Bigdata based REconstruction/redevelopment Decision support system

## Overview
Sample program to build MySQL and Fast API environment with DockerCompose

## Install
Create and Running

add `.env` file and add configs 
```
# .env example

# 뉴스 api 수집을 위한 api id,pw
NEWS_CLIENT_ID = OsLOua238f8IXy9nanMl
NEWS_CLIENT_PW = GTaGmO7nii

MYSQL_DATABASE=fastapi
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=password
MYSQL_HOST=db
# construction table 수집을 위한 api key
CONSTRUCTION_SERVICE_KEY = 457570424d6b756e36376345746541
```

run docker-compose
```
$ make up
```

## DB migration  
before migration, fix fastapi code

```
# access fastapi docker
$ docker exec -it fastapi /bin/bash

# inside of fastapi docker
# move to src directory
> cd ..

# generate revision file
> alembic revision -m "message"

# change revision file in /migration/versions

# run migration
> alembic upgrade head

```
