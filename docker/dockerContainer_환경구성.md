# Docker Container 
## Docker Contrainer 환경구성
### 1.1 네트워크 설정
- ProducerNetwork라는 커스텀 네트워크를 생성 후 Airflow, Kafka의 동일한 네트워크로 설정하여 통신
- Network Driver : bridge

### 1.2 Kafka 설정
- broker1, broker2, broker3 : confluentinc/cp-kafka:7.0.1  image 사용
- Listener
   - Internal : broker1:29092 (airflow와 연결)
   - external : ${DOCKER_HOST_IP:-127.0.0.1}:9092 (local에 설치된 spark와 연결)
- zookeeper : zookeeper:3.8 image 사용
- kafdrop : obsidiandynamics/kafdrop image 사용
