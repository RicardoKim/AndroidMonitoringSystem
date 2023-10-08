from kafka import KafkaProducer
from json import dumps
import subprocess
import re
import threading
from datetime import datetime

# Create a single producer for system resource info
resource_producer = KafkaProducer(
    acks=0,
    api_version=(0, 11, 5),
    client_id='Android_System_Resource',
    compression_type='gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer=None,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

# Keep the existing producer for error logs
error_logcat_producer = KafkaProducer(
    acks=0,
    api_version=(0, 11, 5),
    client_id='Android_Error_Log',
    compression_type='gzip',
    bootstrap_servers=['localhost:29092'],
    key_serializer=None,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

package_name_list = []

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

def extract_resource_info():
    print("Extract Resource Info Begin")
    cpu_command = "adb shell dumpsys cpuinfo | grep 'TOTAL'"
    battery_command = "adb shell dumpsys battery | grep level"
    adb_process = subprocess.Popen(['adb', 'shell', 'top', '-m', '20'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    while True:

       
        log = adb_process.stdout.readline().decode().strip()
        if "Mem" in log:
            memory_info = parse_memory_line(log)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Collect CPU info
            
            cpu_usage_line = subprocess.check_output(cpu_command, shell=True).decode('utf-8').split('\n')[0]
            cpu_usage = cpu_usage_line.split('%')[0].strip()
            # Collect Battery info
            
            battery_result = subprocess.run(battery_command, shell=True, text=True, capture_output=True).stdout.strip()
            battery_level = battery_result.split(":")[1].strip()
            
            # Bundle all info into a single JSON and send to producer
            resource_info = {
                'created_at': now,
                'memory_info': memory_info,
                'cpu_usage': cpu_usage,
                'battery_level': battery_level
            }

            print(resource_info)
            resource_producer.send('Android_System_Resource', value=resource_info)
    return


def extract_error_logcat():
    print('Extract Error Log Begin')
    adb_process = subprocess.Popen(['adb', 'logcat', '*:E'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line = adb_process.stdout.readline()
        if any(pkg_name in line for pkg_name in package_name_list):
            error_logcat_producer.send(
                'Android_Error_Log',
                value = line
            )
    return


if __name__ == "__main__":
    package_process = subprocess.Popen(['adb', 'shell', 'pm', 'list', 'packages', '--user', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = package_process.communicate()
    output = stdout.decode('utf-8')

    packages = re.findall(r'package:([\w\.-]+)', output)

    package_name_list.extend(packages)
    
    try:
        resource_info_thread = threading.Thread(target=extract_resource_info)
        error_logcat_thread = threading.Thread(target=extract_error_logcat)
        resource_info_thread.start()
        error_logcat_thread.start()
    except:
        resource_info_thread.join()
        error_logcat_thread.join()
    
