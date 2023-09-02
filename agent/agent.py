import os
import subprocess
import configparser
import multiprocessing
import logging

PROCESS_LIST = []

def extract_logcat(buffer_name, log_file_path):
    # adb logcat 명령을 실행하여 로그를 추출합니다.
    adb_process = subprocess.Popen(['adb', 'logcat', '-b', buffer_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 로그를 파일에 기록
    with open(log_file_path, 'w') as file:
        try:
            while True:
                # adb logcat 출력을 읽음
                
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

#adb shell top -m 20 명령어로 지속적으로 안드로이드 폰의 프로세스 상태를 log파일로 저장하고 싶어
def extract_top(log_file_path):
    # adb shell top -m 20 명령을 실행하여 로그를 추출합니다.
    adb_process = subprocess.Popen(['adb', 'shell', 'top', '-m', '20'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 로그를 파일에 기록
    with open(log_file_path, 'w') as file:
        try:
            while True:
                # adb shell top -m 20 출력을 읽음
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

    try :
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
        # log 디렉토리 가져오기
        log_root_dict = {}
        log_root_dict["main"] = os.path.join(log_root, config.get('adb', 'main_log_dir'))
        log_root_dict["crash"] = os.path.join(log_root, config.get('adb', 'crash_log_dir'))
        log_root_dict["system"] = os.path.join(log_root, config.get('adb', 'system_log_dir'))
        log_root_dict["process"] = os.path.join(log_root, config.get('adb', 'process_log_dir'))



        for buffer in ['main', 'crash', 'system']:
            log_path = log_root_dict[buffer]
            process = multiprocessing.Process(target=extract_logcat, args=(buffer, log_path))
            process.start()
            PROCESS_LIST.append(process)
        
        log_path = log_root_dict["process"]
        process = multiprocessing.Process(target=extract_top, args=(log_path,))
        process.start()
        PROCESS_LIST.append(process)


    except KeyboardInterrupt as ki:
        # 서브 프로세스 종료
        for process_name in PROCESS_LIST :
            process_name.join()