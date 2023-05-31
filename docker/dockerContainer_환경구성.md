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

### 1.3 Airflow 설정
- Airflow Image : Custom Image (apache/airflow: 2.6.1)
   - Dockerfile과 requriements.txt를 작성하여 airflow 2.6.1 버전에 필요한 Python Library를 추가하여 Custom Image build 및 사용 
- postgres : Airflow의 메타데이터를 저장하는 데이터베이스로 PostgreSQL을 사용
- redis : Airflow worker 및 작업 큐를 위한 메시지 브로커로 Redis를 사용
- airflow-webserver : 사용자가 워크플로우를 실행하고 모니터링할 수 있는 웹 인터페이스를 제공
- aiflow-scheduler : Airflow 스케줄러로, 정의된 워크플로우를 예약하고 실행
- airflow-worker : CeleryExecutor를 사용하여 작업을 분산 처리
- airflow-triggerer : Airflow 트리거러로, 예약된 작업을 자동으로 트리거하고 실행
- airflow-init : Airflow 초기화 서비스로, 데이터베이스 마이그레이션 및 초기 사용자 계정 설정을 담당
