# Airflow를 이용하여 Kafka Producer 배치 작업
## 1. Kakfa
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
<img src="../Images/topic_list.png" alt="이미지" width="600" height="200">
</p>

### 1.3 Kafka Producer 개발
- find_userName : 각 티어별 유저들의 SummonerName List를 만드는 함수
- send_data_to_kafka : 유저의 게임 History Data를 파싱하고 Kafka topic으로 전달하는 Producer
```python
def find_userName(queueType, page):
    userList = riotApi.allTierUsersId(queueType, page)
    return userList


def send_data_to_kafka(**kwargs):
    ti = kwargs['ti']
    userList = ti.xcom_pull(task_ids='find_summonerName')
    #riotApi = RiotMatchData()
    
    producer = KafkaProducer(
        acks=0, 
        compression_type='gzip', 
        bootstrap_servers=['broker1:29092'], 
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )
    
    start = 0
    count = 5
    
    matchRecordData = riotApi.matchDataInfo(userList, start, count)
    print('DATA : ' , matchRecordData)
    
    for data in matchRecordData:  
        recordData_ = data
        producer.send('ypgg',value=recordData_)
        producer.flush()
    #producer.close()
    print("DONE")
```
