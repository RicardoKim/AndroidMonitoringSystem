from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

# SparkSession을 생성합니다.
spark = SparkSession.builder \
    .appName("KafkaTopicConsumer") \
    .getOrCreate()

# Kafka 설정 정보를 설정합니다.
kafka_params = {
    "kafka.bootstrap.servers": "kafka:9092",
    "subscribe": "Android_Task"  # 여기에 Kafka 토픽 이름을 지정하세요.
}

# 스트리밍 데이터를 읽어옵니다.
raw_stream = spark.readStream.format("kafka").options(**kafka_params).load()

# 읽어온 데이터의 값 부분을 JSON 형식으로 변환합니다.
value_schema = StructType([StructField("value", StringType(), True)])
json_stream = raw_stream.selectExpr("CAST(value AS STRING) AS json") \
    .select(from_json("json", value_schema).alias("data")) \
    .select("data.*")

# 데이터를 출력하거나 원하는 작업을 수행합니다.
query = json_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# 스트리밍 작업을 시작합니다.
query.awaitTermination()
