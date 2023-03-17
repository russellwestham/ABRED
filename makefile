up:
	@docker-compose down
	@docker-compose up --build fastapi 
reload:
	@docker-compose up --build fastapi