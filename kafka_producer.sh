source ./env_params.sh

java -cp /usr/lib/kafka/libs/*:KafkaProducer.jar com.example.bigdata.TestProducer "$MAIN_INPUT_PATH" "$KAFKA_PRODUCER_SLEEP_TIME" "$KAFKA_MAIN_TOPIC_NAME" 1 "$KAFKA_BOOTSTRAP_SERVER"