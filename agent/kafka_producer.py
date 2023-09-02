#1. adb로 프로세스 정보를 읽는다
#2. process 정보 관련 토픽을 생성한다.
#3. 토픽에 adb로 읽은 정보를 보내게 된다.
import subprocess
import time

from kafka import KafkaProducer
from json import dumps

producer = KafkaProducer(
    acks = 0,
    client_id = 'test',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

task_producer = KafkaProducer(
    acks = 0,
    client_id = 'Android_Task',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

mem_producer = KafkaProducer(
    acks = 0,
    client_id = 'Android_Mem',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

swap_producer = KafkaProducer(
    acks = 0,
    client_id = 'Android_Swap',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

process_producer = KafkaProducer(
    acks = 0,
    client_id = 'Android_Process',
    compression_type = 'gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer = None,
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

def extract_top():
    section = ""
    last_log = ""
    adb_process = subprocess.Popen(['adb', 'shell', 'top', '-m', '10'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        log = adb_process.stdout.readline().decode().strip()
        if log != last_log:
            last_section = section
            prefix = log
            if "Task" in prefix :
                section = "Task"
                task_producer.send('Android_Task', {
                    section : log
                })
            elif "Mem" in prefix:
                section = "Memory"
                task_producer.send('Android_Mem', {
                    section : log
                })
            elif "Swap" in prefix:
                section = "Swap"
                task_producer.send('Android_Swap', {
                    section : log
                })
            elif "PID" in prefix :
                section = "Process"
            elif last_section == "Process" :
                task_producer.send('Android_Process', {
                    section : log
                })
            else :
                pass
            last_log = log

if __name__ == "__main__":
    extract_top()


    
