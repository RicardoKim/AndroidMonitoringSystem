import os
import subprocess
import configparser
import multiprocessing
import logging

PROCESS_LIST = []

def extract_log_from_device(log_file_path):
    # adb logcat 명령을 실행하여 로그를 추출합니다.
    adb_process = subprocess.Popen(['adb', 'shell','top', '-m', '20'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 로그를 파일에 기록
    with open(log_file_path, 'w') as file:
        try:
            while True:
                # adb logcat 출력을 읽음
                output = adb_process.stdout.readline().decode().strip()
                # logging.INFO(output)
                if output:
                    # 로그를 파일에 기록
                    file.write(output + '\n')
                    file.flush()
                
        except KeyboardInterrupt:
            os.remove(log_file_path)
            adb_process.terminate()
            # logging.DEBUG("Process Terminate")
        # except OSError:
            # logging.WARN("File cannot be deleted")

    return

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return
    else:
        return

if __name__ == "__main__":

    # agent.py 런타임 디렉토리를 상위경로로 이동시킨다.
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    os.chdir(parent_dir)

    # config.ini에서 로그를 저장할 경로를 가져온다.
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # data/log 디렉토리 생성
    data_root = config.get('adb', 'data_root')
    log_root = config.get('adb', 'log_root')
    log_root = os.path.join(data_root, log_root)
    create_directory_if_not_exists(log_root)
    process_log_root = os.path.join(log_root, config.get('adb', 'process_log_root'))
    extract_log_from_device(process_log_root)