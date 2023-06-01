# Spark Streaming
## Spark를 이용한 데이터 집계
### 1. 누적 데이터 집계 연산
- **`spark.catalog.refreshTable("lol_table_text")`**: 함수를 사용하여 "lol_table_text" 테이블을 새로 고침 함. 이를 통해 테이블의 메타데이터를 업데이트하고 최신 정보를 가져온다.
- **`df_all_lol_warehouse = spark.read.json(spark.table("lol_table_text").select("history").rdd.flatMap(lambda x: x))`**: "lol_table_text" 테이블에서 "history" 열을 선택하고, 각 레코드의 값을 하나의 JSON 문자열로 변환 후, **`spark.read.json()`** 함수를 사용하여 JSON 형식의 데이터를 DataFrame으로 읽어온다.
- **`rdd.flatMap(lambda x: x)`**: RDD에서 각 요소를 flatten하여 단일 요소로 만들어주는 역할
- **`withColumn("컬럼명", col("championInfo").getItem("컬럼명"))`:** "championInfo" 열에서 값을 추출하여 새로운 컬럼 생성
- **`df_all_lol_warehouse = df_all_lol_warehouse.drop("championInfo")`**: "championInfo" 컬럼을 삭제
```python
from pyspark.sql.functions import col

spark.catalog.refreshTable("lol_table_text")

df_all_lol_warehouse = spark.read.json(spark.table("lol_table_text").select("history").rdd.flatMap(lambda x: x))

df_all_lol_warehouse = df_all_lol_warehouse \
  .withColumn("champion_name", col("championInfo").getItem("championName")) \
  .withColumn("champion_level", col("championInfo").getItem("championLevel")) \
  .withColumn("kill_streak", col("championInfo").getItem("killStreak")) \
  .withColumn("kill", col("championInfo").getItem("kill")) \
  .withColumn("death", col("championInfo").getItem("death")) \
  .withColumn("assist", col("championInfo").getItem("assist")) \
  .withColumn("vision_ward_count", col("championInfo").getItem("visionWardCount")) \
  .withColumn("minion_count", col("championInfo").getItem("minionCOunt")) \
  .withColumn("spell_1", col("championInfo").getItem("spells").getItem(0).getItem(0)) \
  .withColumn("spell_2", col("championInfo").getItem("spells").getItem(1).getItem(0)) \
  .withColumn("items_1", col("championInfo").getItem("items").getItem(0)) \
  .withColumn("items_2", col("championInfo").getItem("items").getItem(1)) \
  .withColumn("items_3", col("championInfo").getItem("items").getItem(2)) \
  .withColumn("items_4", col("championInfo").getItem("items").getItem(3)) \
  .withColumn("items_5", col("championInfo").getItem("items").getItem(4)) \
  .withColumn("items_6", col("championInfo").getItem("items").getItem(5)) \
  .withColumn("items_7", col("championInfo").getItem("items").getItem(6)) \
  .withColumn("primary_rune", col("championInfo").getItem("runes").getItem("primaryRunes").getItem(1)) \
  .withColumn("sub_rune", col("championInfo").getItem("runes").getItem("subRunes").getItem(0)) 

df_all_lol_warehouse = df_all_lol_warehouse.drop("championInfo")

z.show(df_all_lol_warehouse)
```
