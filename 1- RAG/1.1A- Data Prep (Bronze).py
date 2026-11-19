# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

datasource = [f'{project.dataset_volume}/{folder}'
              for folder in ['guias', 'matrices', 'troubleshooting']]
print(datasource)

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

docs_raw_df = (spark.read.format("binaryfile")
                .load(datasource)
                .withColumn("ingestion_time", current_timestamp()))

display(docs_raw_df.orderBy("length"))

# COMMAND ----------

docs_raw_df.write.mode("overwrite").saveAsTable("bronze_docs_raw")