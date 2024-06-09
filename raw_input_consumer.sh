#!/bin/bash

# Source the environment variables
source ./env_params.sh

# Run the Python consumer
python raw_input_consumer.py "$KAFKA_MAIN_TOPIC_NAME" "$KAFKA_BOOTSTRAP_SERVER"
