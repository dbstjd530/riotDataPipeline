# Spark Streaming
## Spark를 이용한 데이터 집계
### 1. 누적 데이터 집계 연산
- **`spark.catalog.refreshTable("lol_table_text")`**: 함수를 사용하여 "lol_table_text" 테이블을 새로 고침 함. 이를 통해 테이블의 메타데이터를 업데이트하고 최신 정보를 가져온다.
- **`df_all_lol_warehouse = spark.read.json(spark.table("lol_table_text").select("history").rdd.flatMap(lambda x: x))`**: "lol_table_text" 테이블에서 "history" 열을 선택하고, 각 레코드의 값을 하나의 JSON 문자열로 변환 후, **`spark.read.json()`** 함수를 사용하여 JSON 형식의 데이터를 DataFrame으로 읽어온다.
- **`rdd.flatMap(lambda x: x)`**: RDD에서 각 요소를 flatten하여 단일 요소로 만들어주는 역할
- **`withColumn("컬럼명", col("championInfo").getItem("컬럼명"))`:** "championInfo" 열에서 값을 추출하여 새로운 컬럼 생성
- **`df_all_lol_warehouse = df_all_lol_warehouse.drop("championInfo")`**: "championInfo" 컬럼을 삭제
