# ksd-OCR-Reader-Server

## Service 등록하기
### service file 생성
```
# sudo nano /etc/systemd/system/ksdserver.service
[Unit]
Description=Run ksd-naver-ocr-server

[Service]
Type=simple
WorkingDirectory=/home/ec2-user/service/ksd-OCR-Reader-Server
ExecStart=/bin/bash /home/ec2-user/service/ksd-OCR-Reader-Server/init.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Service 등록하기

```
sudo systemctl start ksdserver.service
```
### Service 등록 확인하기

```
sudo systemctl status ksdserver.service
```
```buildoutcfg
# result
[ec2-user@ip-0-0-0-0 ksd-OCR-Reader-Server]$ sudo systemctl status ksdserver.service 
● ksdserver.service - Run ksd-naver-ocr-server
   Loaded: loaded (/etc/systemd/system/ksdserver.service; disabled; vendor preset: disabled)
   Active: active (running) since 화 1900-01-01 01:01:01 UTC; 7s ago
 Main PID: 10761 (bash)
   CGroup: /system.slice/ksdserver.service
           ├─10761 /bin/bash /home/ec2-user/service/ksd-OCR-Reader-Server/init.sh
           ├─10767 /home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/python3 /home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/uvicorn KsdNaverOCRServer.main:app --reload --host 0.0.0.0
           ├─10768 /home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/python3 -c from multiprocessing.semaphore_tracker import main;main(4)
           └─10769 /home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/python3 -c from multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=5, pipe_handle=7) --multiprocessing-fork

11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: Requirement already satisfied: uvicorn==0.13.4 in ./venv/lib/python3.7/site-packages (from -r requirements.txt (line 30)) (0.13.4)
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: Requirement already satisfied: importlib-metadata; python_version < "3.8" in ./venv/lib/python3.7/site-packages (from SQLAlchemy==1.4.11->-r requirements.txt (line 26)) (4.8.1)
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: Requirement already satisfied: zipp>=0.5 in ./venv/lib/python3.7/site-packages (from importlib-metadata; python_version < "3.8"->SQLAlchemy==1.4.11->-r requirements.txt (line 26)) (3.6.0)
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: WARNING: You are using pip version 20.1.1; however, version 21.3.1 is available.
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: You should consider upgrading via the '/home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/python3 -m pip install --upgrade pip' command.
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
11월 30 14:54:30 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: INFO:     Started reloader process [10767] using statreload
11월 30 14:54:31 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: INFO:     Started server process [10769]
11월 30 14:54:31 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: INFO:     Waiting for application startup.
11월 30 14:54:31 ip-0-0-0-0.ap-northeast-2.compute.internal bash[10761]: INFO:     Application startup complete.
```

-----
