# ABRED
 AI-Bigdata based REconstruction/redevelopment Decision support system

## Overview
Sample program to build MySQL and Fast API environment with DockerCompose

## Install
Create and Running

add `.env` file and add configs 
```
# .env example
MYSQL_DATABASE=fastapi
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=password
MYSQL_HOST=db
```

run docker-compose
```
$ make up
```

## DB migration  
befor migration, fix fastapi code

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
