from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType
from pymongo import MongoClient
from pyspark.sql.functions import regexp_extract

def write_to_mongo(df, epoch_id):
    mongo_client = MongoClient('mongodb://root:1234@mongodb1:27017')  # Docker Compose 서비스 이름과 포트를 사용하여 MongoDB에 연결합니다.
    db = mongo_client.AndroidLogDataMart  # Database를 선택합니다.
    collection = db.AndroidErrorLogMonitoring  # Collection을 선택합니다.
    
    data = df.collect()  # Spark DataFrame을 Python 리스트로 변환합니다.
    for row in data:
        collection.insert_one(row.asDict())  # 각 로우를 MongoDB에 삽입합니다.

# SparkSession을 생성합니다.
spark = SparkSession.builder \
    .appName("AndroidErrorLogTopicConsumer") \
    .getOrCreate()

# Kafka 설정 정보를 설정합니다.
memory_kafka_params = {
    "kafka.bootstrap.servers": "kafka:9092",
    "subscribe": "Android_Error_Log"  # 여기에 Kafka 토픽 이름을 지정하세요.
}

# 스트리밍 데이터를 읽어옵니다.
raw_stream = spark.readStream.format("kafka").options(**memory_kafka_params).load()

parsed_stream = raw_stream.selectExpr("CAST(value AS STRING) as value") \
    .withColumn("date", regexp_extract("value", r"(\d{2}-\d{2})", 1)) \
    .withColumn("time", regexp_extract("value", r"(\d{2}:\d{2}:\d{2}.\d{3})", 1)) \
    .withColumn("error_info", regexp_extract("value", r"E (\S+:\s.*)", 1))

# 필요한 필드만 선택하여 구조를 변경합니다.
transformed_stream = parsed_stream.select("date", "time", "error_info")

# 데이터를 출력하거나 원하는 작업을 수행합니다.
query = transformed_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_mongo) \
    .start()

# 스트리밍 작업을 시작합니다.
query.awaitTermination()
