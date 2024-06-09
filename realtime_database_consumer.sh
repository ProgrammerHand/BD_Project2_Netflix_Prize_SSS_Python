source ./env_params.sh

python realtime_database_consumer.py "$DB_HOST" "$DB_PORT" "$DB_NAME" "$DB_TABLE_NAME" "$DB_USER" "$DB_USER_PASSWORD"
