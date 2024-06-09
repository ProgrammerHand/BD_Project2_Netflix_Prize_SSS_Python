source ./env_params.sh

$SPARK_HOME/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.6.0 \
  sss_engine.py \
  "$SUPPORT_FILE_PATH" \
  "$DELAY_MODE" \
  "$KAFKA_BOOTSTRAP_SERVER" \
  "$KAFKA_MAIN_TOPIC_NAME" \
  "$DB_NAME" \
  "$DB_PORT" \
  "$DB_TABLE_NAME" \
  "$DB_USER" \
  "$DB_USER_PASSWORD" \
  "$WINDOW_SIZE" \

