#restart container agent-api
rs:
	docker restart agent-api
#log agent-api
log:
	docker logs agent-api
#clear log agent-api
clearlog:
	sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' agent-api)
#exec container agent-api
e:
	docker exec -it agent-api bash
#docker compose
down:
	docker-compose down

up:
	docker-compose up -d
