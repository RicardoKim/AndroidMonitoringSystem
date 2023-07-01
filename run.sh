#restart adb server
adb kill-server
adb start-server&

#run agent that pull data from user phone
cd agent
python agent.py&

cd ..
#run ELK stack
docker-compose up&
