from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, DateType
from pymongo import MongoClient

def write_to_mongo(df, epoch_id, collection_name):
    mongo_client = MongoClient('mongodb://root:1234@mongodb1:27017')
    db = mongo_client.AndroidLogDataMart
    collection = db[collection_name]
    
    data = df.collect()
    for row in data:
        collection.insert_one(row.asDict())

# SparkSession을 생성합니다.
spark = SparkSession.builder \
    .appName("AndroidLogTopicConsumer") \
    .getOrCreate()

# Kafka 설정 정보를 설정합니다.
kafka_params = {
    "kafka.bootstrap.servers": "kafka:9092",
    "subscribe": "Android_System_Resource"
}

# 스트리밍 데이터를 읽어옵니다.
raw_stream = spark.readStream.format("kafka").options(**kafka_params).load()

# 읽어온 데이터의 값 부분을 JSON 형식으로 변환합니다.
resource_value_schema = StructType([
    StructField("created_at", StringType(), True), 
    StructField("memory_info", StructType(
        [
            StructField("Total", FloatType(), True),
            StructField("Used", FloatType(), True),
            StructField("Free", FloatType(), True)
        ]
    ), True), 
    StructField("cpu_usage", StringType(), True),
    StructField("battery_level", StringType(), True)
])

# Resource 정보와 Error 로그를 처리합니다.
resource_stream = raw_stream \
    .filter(col("topic") == "Android_System_Resource") \
    .selectExpr("CAST(value AS STRING) AS json") \
    .select(from_json("json", resource_value_schema).alias("data")) \
    .select("data.*")

# MongoDB에 Resource 정보를 저장합니다.
resource_query = resource_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: write_to_mongo(df, epoch_id, "AndroidResourceMonitoring")) \
    .start()

# 스트리밍 작업을 시작합니다.
spark.streams.awaitAnyTermination()
