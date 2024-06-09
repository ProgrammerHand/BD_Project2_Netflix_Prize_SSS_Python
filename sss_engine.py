from pyspark.sql import SparkSession
from pyspark.sql.functions import unix_timestamp, window, approx_count_distinct, col, from_csv, sum as spark_sum, count as spark_count
from pyspark.sql.types import StructType, IntegerType, TimestampType, StructField
import socket
import sys

def save_to_database(partDF, database_url, databaseProperties, database_table_name, mode="append"):
    partDF \
    .write \
    .mode(mode) \
    .jdbc(database_url, database_table_name, properties=databaseProperties)

def write_stream_to_db(df, mode, delay, url, db_properties, table_name):
    return df \
        .writeStream \
        .outputMode(mode) \
        .foreachBatch(lambda partDF, partId: save_to_database(partDF, url, db_properties, table_name)) \
        .option("checkpointLocation", "/tmp/checkpoints/aggregatedRatings") \
        .trigger(processingTime=delay) \
        .start()

def data_processing(scoresDF, support_file, database_url, database_user, database_user_password, delay_mode, window_size, database_table_name):

    aggregatedScoresDF = scoresDF
    
    if delay_mode == "C":
        aggregatedScoresDF = scoresDF.withWatermark("date", "3 days")

    aggregatedScoresDF = aggregatedScoresDF.groupBy(window("date", f"{window_size} days"), "film_id") \
        .agg(
        spark_count("*").alias("scores_count"),
        spark_sum("rate").alias("scores_sum"),
        approx_count_distinct("rate").alias("unique_scores_count")
    ) \
        .join(support_file, aggregatedScoresDF.film_id == support_file["_c0"], "inner") \
        .select(
            unix_timestamp(col("window.start")).alias("window_start"),
            "film_id",
            col("_c2").alias("title"),
            "scores_sum",
            "scores_count",
            "unique_scores_count"
            )

    databaseProperties = {
        "user": database_user,
        "password": database_user_password,
        "driver": "org.postgresql.Driver"
    }

    if delay_mode == "A":
        query = write_stream_to_db(aggregatedScoresDF, "update", "15 seconds", database_url, databaseProperties, database_table_name)

    if delay_mode == "C":
        query = write_stream_to_db(aggregatedScoresDF, "append", "30 second", database_url, databaseProperties, database_table_name)

def main():
    if len(sys.argv) != 11:
        raise Exception("Usage: script <support_file_path> <delay_mode> <kafka_bootstrap_server> <kafka_topic> <database_name> <database_port> <database_user> <database_table_name> <database_password> <window_size>")

    support_file_path = sys.argv[1]
    delay_mode = sys.argv[2]
    kafka_bootstrap_server = sys.argv[3]
    kafka_topic = sys.argv[4]
    database_name = sys.argv[5]
    database_port = sys.argv[6]
    database_table_name = sys.argv[7]
    database_user = sys.argv[8]
    database_user_password = sys.argv[9]
    window_size = int(sys.argv[10])

    spark_session = SparkSession.builder \
        .appName("Netflix data processing engine") \
        .getOrCreate()
    
    host_name = socket.gethostname()

    kafkaDF = spark_session.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", f"{host_name}:9092") \
        .option("subscribe", kafka_topic) \
        .load()

    valueDF = kafkaDF.selectExpr("CAST(value AS STRING) as value")

    dataSchema = StructType([
        StructField("date", TimestampType(), True),
        StructField("film_id", IntegerType(), True),
        StructField("user_id", IntegerType(), True),
        StructField("rate", IntegerType(), True),
    ])

    scoresDF = valueDF.select(
        from_csv(col("value"), dataSchema.simpleString()).alias("val")
    ).select(
        col("val.date"),
        col("val.film_id"),
        col("val.user_id"),
        col("val.rate"),
    )

    scoresDF.printSchema()
    support_file = spark_session.read.option("header", False).csv(support_file_path)
    support_file.printSchema()

    database_url = f"jdbc:postgresql://{host_name}:{database_port}/{database_name}"
    data_processing(scoresDF, support_file, database_url, database_user, database_user_password, delay_mode, window_size, database_table_name)

    spark_session.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()