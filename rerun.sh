# docker-compose down -v
# docker-compose up -d --build
docker stop sssp-backend
docker rm -f sssp-backend
docker-compose up -d --build
