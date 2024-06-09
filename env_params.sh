#!/bin/bash
# cloud parameters
echo "Cluster/GCS parameters creating?"
export BUCKET_NAME="pbds-24-dp"
export CLUSTER_NAME=$(/usr/share/google/get_metadata_value attributes/dataproc-cluster-name)
export HADOOP_CONFIG_DIR=/etc/hadoop/conf
export HADOOP_CLASSPATH=`hadoop classpath`
export MAIN_INPUT_PATH="$HOME/netflix-prize-data"
export SUPPORT_INPUT_PATH="$HOME/movie_titles.csv"
export SUPPORT_FILE_PATH="gs://${BUCKET_NAME}/movie_titles.csv"
echo "Cluster/GCS parameters created!"

# kafka parameters
echo "Kafka parameters creating?"
export KAFKA_MAIN_TOPIC_NAME="netflix-prize-scores"
export KAFKA_BOOTSTRAP_SERVER="${CLUSTER_NAME}-w-0:9092"
export KAFKA_PRODUCER_SLEEP_TIME=30
echo "Kafka parameters created!"

# JDBC parameters
echo "DB parameters creating?"
export DB_URL="jdbc:postgresql://localhost:8432/netflix_ratings"
export DB_HOST="localhost"
export DB_PORT="8432"
export DB_NAME="netflix_prize_data"
export DB_TABLE_NAME="film_scores"
export DB_USER="engineuser"
export DB_USER_PASSWORD="stream"
export PGPASSWORD='mysecretpassword'
echo "DB parameters created!"

# processing engine parameters
echo "SSS engine parmetrs creating?"
export WINDOW_SIZE=30
export DELAY_MODE="A"
echo "SSS engine parameters created!"