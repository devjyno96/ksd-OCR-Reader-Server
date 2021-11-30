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
ExecStart=/home/ec2-user/service/ksd-OCR-Reader-Server/venv/bin/python3 /home/ec2-user/service/ksd-OCR-Reader-Server/bin/run.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### Service 등록하기

```
systemctl start ksdserver.service
```

-----

## 1. 필요 기능

1. POST "/ocr/request/"

   S3에 업로드 된 사진 URL과 사진 유형(지능, 자폐 등)을 보내준다.
