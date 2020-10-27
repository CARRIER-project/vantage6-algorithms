REGULAR_TAG=localhost:5000/v6-carrier-py
SPARQL_TAG=localhost:5000/v6-carrier-py-sparql

# Build images
docker build -t $REGULAR_TAG --no-cache .
docker build -t $SPARQL_TAG --no-cache -f Dockerfile.sparql .

docker push $REGULAR_TAG
docker push $SPARQL_TAG
