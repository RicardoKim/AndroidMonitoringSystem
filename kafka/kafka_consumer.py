from kafka import KafkaConsumer
from json import loads

android_task_consumer = KafkaConsumer(
    'Android_Error_Log',
    api_version = (0,11,5),
    bootstrap_servers=['localhost:29092'],
    auto_offset_reset = 'earliest',
    enable_auto_commit=True,
    group_id='test_group',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1000
)

def consume():
    for android_task_message in android_task_consumer:
        print(android_task_message.value)

if __name__ == "__main__":
    consume()