#/bin/bash
docker compose down
docker volume ls 
docker volume rm sentinel_pgdata 
docker compose up --build -d
