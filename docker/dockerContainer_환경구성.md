# Docker Container 
## Docker Contrainer 환경구성
### 1.1 네트워크 설정
- ProducerNetwork라는 커스텀 네트워크를 생성 후 Airflow, Kafka의 동일한 네트워크로 설정하여 통신
- Network Driver : bridge
