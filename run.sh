#!/bin/bash

# # 쉘 종류 확인
# SHELL_NAME=$(basename "$SHELL")

# # conda init 실행
# case "$SHELL_NAME" in
#     bash)
#         conda init bash
#         ;;
#     zsh)
#         conda init zsh
#         ;;
#     fish)
#         conda init fish
#         ;;
#     *)
#         echo "Unsupported shell: $SHELL_NAME"
#         exit 1
#         ;;
# esac

# # 새로운 터미널 세션에서 변경 사항을 적용하기 위해 스크립트 실행
# exec "$SHELL"

# # conda activate 수행
# conda activate AMS

#restart adb server
adb kill-server
adb start-server&

#run agent that pull data from user phone
cd agent
python agent.py&

cd ..
#run ELK stack
docker-compose up&
