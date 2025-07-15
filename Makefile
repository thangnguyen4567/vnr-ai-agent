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

# Chạy test api 
test:
	docker exec -it agent-api pytest -v
	
# Kiểm tra độ bao phủ code của test
test-cov:
	docker exec -it agent-api pytest --cov=src tests/ --cov-report term-missing

st:
	docker exec -it agent-api streamlit run app.py

graph:
	docker exec -it agent-api python graph.py
