from datetime import datetime
from airflow import DAG
from kafka import KafkaProducer
from airflow.operators.python import PythonOperator
from json import dumps
from riotmatchapi import RiotMatchData
import requests
#from airflow_provider_kafka.operators.produce_to_topic import ProduceToTopicOperator


api_key = 'RGAPI-a0b17c3a-858a-43b1-bc81-3b55a768124b'

request_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

riotApi = RiotMatchData()


def print_hello(val):
    print(f'hello {val}...')

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
    

default_args = {
    'start_date': datetime(2023, 5, 15)
}
    

with DAG(
    dag_id='riot_pipeline',
    schedule_interval='*/10 * * * *',
    catchup=False,
    default_args=default_args
) as dag:
    
    run_python1 = PythonOperator(
        task_id='run_python1',
        python_callable=print_hello,
        op_kwargs={'val': 'airflow'},
        dag=dag
    )
    
    find_summonerName = PythonOperator(
        task_id = 'find_summonerName',
        python_callable=find_userName,
        op_kwargs={'queueType': 'RANKED_SOLO_5x5', 'page': 1},
        provide_context=True,
        dag=dag
    )
    
    send_data_task = PythonOperator(
        task_id='send_data_task',
        python_callable=send_data_to_kafka,
        dag=dag
    )
    
    run_python1 >> find_summonerName >> send_data_task

