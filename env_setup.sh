echo "Extracting env params from env_params.sh?"
source ./env_params.sh
echo "Env params extracted!"

echo "Installing python libraries?"
pip3 install kafka-python
pip3 install psycopg2
echo "libraries installed!"

echo "Creating input directory?"
mkdir "$MAIN_INPUT_PATH"
echo "Input directory created!"

echo "Copying input files from GCS?"
hadoop fs -copyToLocal gs://"${BUCKET_NAME}"/movie_titles.csv "$SUPPORT_INPUT_PATH"
hadoop fs -copyToLocal gs://"${BUCKET_NAME}"/netflix-prize-data/*.csv "$MAIN_INPUT_PATH"
echo "Input files copied!"

echo "Creating Kafka topics?"
kafka-topics.sh --bootstrap-server ${CLUSTER_NAME}-w-1:9092 --create --replication-factor 2 --partitions 2 --topic $KAFKA_MAIN_TOPIC_NAME
echo "Kafka topics created!"

echo "PostgreSQL db container booting?"
docker run --name postgresdb -p 8432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

echo "Container starting..."
sleep 12
echo "DB container started!"

echo "Running DB structure setup script?"
psql -h localhost -p 8432 -U postgres -v user="$DB_USER" -v password="$DB_USER_PASSWORD" -v db_name="$DB_NAME" -f db_setup.sql
echo "DB structure set up!"