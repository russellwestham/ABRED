up:
	@docker-compose down
	@docker-compose up --build fastapi 
reload:
	@docker-compos up --build fastapi