TAG=localhost:5000/v6-carrier-py

# Build image
docker build -t $TAG .

docker push $TAG
