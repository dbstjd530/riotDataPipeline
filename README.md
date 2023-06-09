# League of Legends Data Pipeline
<br />
<h2> Use tech stack 📚 </h2>

![Python](https://img.shields.io/badge/-Python-007ACC?style=for-the-badge&logo=Python&logoColor=ffffff)
![Airflow](https://img.shields.io/badge/-airflow-F05032?style=for-the-badge&logo=Apache-airflow&logoColor=ffffff)
![Kafka](https://img.shields.io/badge/-Kafka-222222?style=for-the-badge&logo=Apache-Kafka)
![Spark](https://img.shields.io/badge/-Spark-F05032?style=for-the-badge&logo=Apache-Spark&logoColor=ffffff)
![Docker](https://img.shields.io/badge/-Docker-46a2f1?style=for-the-badge&logo=docker&logoColor=ffffff)
<br/>

## Pipeline 구성도
<p align="left">
<img src="./Images/pipeline.png" alt="이미지1" width="800" height="400">
</p>

## Notion Link
https://positive-bone-588.notion.site/League-of-Legends-Data-Pipeline-63b69e91e52e41a0908ea7090e7ef2da

### **⚠ 아래의 파랑색 글씨를 누르시면 설명하는 페이지로 넘어갑니다.**
## 1. 데이터 파싱 (Python)
- [데이터 파싱](./python/README.md)

## 2. 데이터 수집 (Kafka, Airflow, Docker)
- [도커 환경구성](./docker/README.md)
- [Kafka Producer 구현](./airflow_kafka/README.md)

## 3. 데이터 저장 및 집계 (Spark)
- [Spark을 이용한 데이터 저장 및 집계](./spark/README.md)



