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

pattern = r'(\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3}) (\w+ \w+): (.+)'

# 로그로부터 필요한 정보를 추출합니다.
extracted_stream = raw_stream.selectExpr("CAST(value AS STRING) AS raw_log") \
    .select(col("raw_log"),
            regexp_extract(col("raw_log"), pattern, 1).alias("Date"),
            regexp_extract(col("raw_log"), pattern, 2).alias("Time"),
            regexp_extract(col("raw_log"), pattern, 3).alias("LogType"),
            regexp_extract(col("raw_log"), pattern, 4).alias("ErrorMessage"))

# 데이터를 MongoDB에 쓰기 위해 foreachBatch()를 사용합니다.
query = extracted_stream.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_mongo) \
    .start()

# 스트리밍 작업을 시작합니다.
query.awaitTermination()
