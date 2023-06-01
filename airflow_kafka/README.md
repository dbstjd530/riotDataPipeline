# Airflow를 이용하여 Kafka Producer 배치 작업
## 1. Airflow를 이용한 배치
### 1.1 Kafka topic 생성
ypgg라는 topic을 생성
```bash
$ kafka-topics --create --topic ypgg --partitions 3 --replication-factor 3  --bootstrap-server broker1:29092
```
### 1.2 Kafka topic list 확인
docker를 사용하므로 broker1 컨테이너에 접속하여 topic 생성이 되었는지 list 확인
```bash
$ docker exec -it broker1 bash
$ kafka-topics --list --bootstrap-server localhost:9092
```
<p align="left">
<img src="../Images/topic_list.png" alt="이미지" width="1500" height="600">
</p>

