# docker-compose down -v
# docker-compose up -d --build
docker-compose stop sssp-backend
docker-compose rm -f sssp-backend
docker-compose up -d --build sssp-backend