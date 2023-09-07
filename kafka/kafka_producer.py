#1. adb로 프로세스 정보를 읽는다
#2. process 정보 관련 토픽을 생성한다.
#3. 토픽에 adb로 읽은 정보를 보내게 된다.
import subprocess
import re

from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'test',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

task_producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'Android_Task',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

mem_producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'Android_Mem',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

swap_producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'Android_Swap',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

process_producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'Android_Process',
    compression_type = 'gzip',
    bootstrap_servers=['kafka:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

def parse_android_top_output(output_str):
    # 각 상태에 대한 정규 표현식 패턴을 정의합니다.
    patterns = {
        "Tasks": r"Tasks:\s*(\d+)\s*total",
        "Running": r"(\d+)\s*running",
        "Sleeping": r"(\d+)\s*sleeping",
        "Stopped": r"(\d+)\s*stopped",
        "Zombie": r"(\d+)\s*zombie"
    }
    
    # 결과를 저장할 딕셔너리를 생성합니다.
    result = {}

    # 각 패턴에 대해 문자열에서 값을 찾아 결과 딕셔너리에 저장합니다.
    for key, pattern in patterns.items():
        match = re.search(pattern, output_str)
        if match:
            result[key] = int(match.group(1))
        else:
            result[key] = None

    return result

def extract_top():
    adb_process = subprocess.Popen(['adb', 'shell', 'top', '-m', '10'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        log = adb_process.stdout.readline().decode().strip()
        if "Task" in log :
            parsed_data = parse_android_top_output(log)
            task_producer.send(
                'Android_Task', 
                    value=parsed_data
                )

if __name__ == "__main__":
    extract_top()


    
