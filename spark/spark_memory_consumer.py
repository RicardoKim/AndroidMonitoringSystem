from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType
from pymongo import MongoClient

def write_to_mongo(df, epoch_id):
    mongo_client = MongoClient('mongodb://root:1234@mongodb1:27017')  # Docker Compose 서비스 이름과 포트를 사용하여 MongoDB에 연결합니다.
    db = mongo_client.AndroidLogDataMart  # Database를 선택합니다.
    collection = db.AndroidMemoryMonitoring  # Collection을 선택합니다.
    
    data = df.collect()  # Spark DataFrame을 Python 리스트로 변환합니다.
    for row in data:
        collection.insert_one(row.asDict())  # 각 로우를 MongoDB에 삽입합니다.

# SparkSession을 생성합니다.
spark = SparkSession.builder \
    .appName("AndroidMemoryTopicConsumer") \
    .getOrCreate()

# Kafka 설정 정보를 설정합니다.
memory_kafka_params = {
    "kafka.bootstrap.servers": "kafka:9092",
    "subscribe": "Android_Memory"  # 여기에 Kafka 토픽 이름을 지정하세요.
}

# 스트리밍 데이터를 읽어옵니다.
raw_stream = spark.readStream.format("kafka").options(**memory_kafka_params).load()

# 읽어온 데이터의 값 부분을 JSON 형식으로 변환합니다.
value_schema = StructType([
    StructField("Total", FloatType(), True),
    StructField("Used", FloatType(), True),
    StructField("Free", FloatType(), True)
])

json_stream = raw_stream.selectExpr("CAST(value AS STRING) AS json") \
    .select(from_json("json", value_schema).alias("data")) \
    .select("data.*")



# 원하는 로직을 적용하여 데이터를 변환합니다.
transformed_stream = json_stream.withColumn("Total", col("Total")) \
    .withColumn("Used", col("Used")) \
    .withColumn("Free", col("Free"))

# 데이터를 출력하거나 원하는 작업을 수행합니다.
query = transformed_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_mongo) \
    .start()

# 스트리밍 작업을 시작합니다.
query.awaitTermination()