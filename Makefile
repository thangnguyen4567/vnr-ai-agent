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
#ignore file settings/llm.yaml
ignore:
	git update-index --skip-worktree settings/llm.yaml
#unignore file settings/llm.yaml
unignore:
	git update-index --no-skip-worktree settings/llm.yaml
#docker compose
down:
	docker-compose down
#docker compose up
up:
	docker-compose up -d
	
#docker compose up --build
up-build:
	docker-compose up -d --build
# Chạy test api 
test:
	docker exec -it agent-api pytest -v
	
# Kiểm tra độ bao phủ code của test
test-cov:
	docker exec -it agent-api pytest --cov=src tests/ --cov-report term-missing

st:
	docker exec -it agent-api streamlit run ui/main.py --server.port 8501

graph:
	docker exec -it agent-api python graph.py

rm-vol:
	docker volume prune
