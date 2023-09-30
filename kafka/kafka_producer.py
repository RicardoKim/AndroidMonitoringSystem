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

process_producer = KafkaProducer(
    acks = 0,
    api_version = (0,11,5),
    client_id = 'Android_Process',
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

def parse_android_process_info(output_str):
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

def parse_memory_line(log):
    pattern = r"Mem:\s+(\d+)K total,\s+(\d+)K used,\s+(\d+)K free"
    matches = re.findall(pattern, log)

    # 추출된 값을 GB 단위로 변환 및 딕셔너리 생성
    def kb_to_gb(kb):
        return round(kb / 1024 / 1024, 2)

    for match in matches:
        total, used, free = match
        total, used, free = map(kb_to_gb, map(int, [total, used, free]))
        return {
            "Total": total,
            "Used": used,
            "Free": free
        }
    return 

# def parse_swap_line(log):
#     pattern = r"Swap:\s+(\d+)K total,\s+(\d+)K used,\s+(\d+)K free"
#     matches = re.findall(pattern, log)

#     # 추출된 값을 GB 단위로 변환 및 딕셔너리 생성
#     def kb_to_gb(kb):
#         return kb / 1024 / 1024

#     result = {}

#     for match in matches:
#         total, used, free = match
#         total, used, free = map(kb_to_gb, map(int, [total, used, free]))
#         result['Swap'] = {
#             "Total": f"{total:.2f} GB",
#             "Used": f"{used:.2f} GB",
#             "Free": f"{free:.2f} GB"
#         }
#     return result

def extract_top():
    adb_process = subprocess.Popen(['adb', 'shell', 'top', '-m', '20'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        log = adb_process.stdout.readline().decode().strip()
        # print(log)
        if "Task" in log :
            parsed_data = parse_android_process_info(log)
            print(parsed_data)
            process_producer.send(
                'Android_Process', 
                value=parsed_data
                )
        elif "Mem" in log:
            parsed_data = parse_memory_line(log)
            print(parsed_data)
            if parsed_data:
                mem_producer.send(
                    'Android_Memory',
                    value = parsed_data
                )
        # elif "Swap" in log:
        #     parsed_data = parse_memory_line(log)
        #     swap_producer.send(
        #         'Android_Swap',
        #         value = parsed_data
        #     )
        

if __name__ == "__main__":
    extract_top()


    
