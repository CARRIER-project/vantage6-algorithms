HOST=$1

REGULAR_TAG=$HOST:443/v6-carrier-py
SPARQL_TAG=$HOST:443/v6-carrier-py-sparql

# Build images
docker build -t $REGULAR_TAG .
docker build -t $SPARQL_TAG -f Dockerfile.sparql .

docker push $REGULAR_TAG
docker push $SPARQL_TAG
