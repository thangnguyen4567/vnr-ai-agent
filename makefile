rs:
	docker restart agent-api
log:
	docker logs agent-api
	
clearlog:
	sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' agent-api)

e:
	docker exec -it agent-api bash

down:
	docker-compose down

up:
	docker-compose up -d
