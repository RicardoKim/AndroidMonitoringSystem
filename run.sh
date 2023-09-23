#!/bin/bash

# MongoDB 데이터 폴더를 삭제하고 새로 만듭니다.
sudo rm -rf ./mongodb &
mkdir ./mongodb &

# 모든 백그라운드 작업이 완료되기를 기다립니다.
wait

# Python 스크립트를 실행합니다.
python3 kafka/kafka_producer.py > kafka_producer.log 2>&1 &

# Docker Compose를 사용하여 서비스를 시작합니다.
docker-compose up -d &

# 모든 백그라운드 작업이 완료되기를 기다립니다.
wait

# app 디렉토리로 이동하고 npm run dev를 실행합니다.
cd app
npm run dev > npm.log 2>&1 &
