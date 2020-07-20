TAG=localhost:5000/v6-carrier-py

# Build image
docker build -t $TAG --no-cache .

docker push $TAG
