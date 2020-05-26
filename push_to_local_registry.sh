TAG=localhost:5001/v6-carrier-py

# Build image
docker build -t $TAG .

docker push $TAG
