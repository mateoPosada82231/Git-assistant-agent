# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

bronze_df = spark.read.table("bronze_docs_raw")
display(bronze_df)

# COMMAND ----------

# DBTITLE 1,Vista previa del texto decodificado
# MAGIC %sql
# MAGIC -- Los documentos son .md, .txt y .csv: ya son texto, no necesitan parseo estructurado.
# MAGIC -- Se decodifican directamente a texto plano (UTF-8).
# MAGIC SELECT path,
# MAGIC        decode(content, 'UTF-8') AS raw_text
# MAGIC FROM bronze_docs_raw

# COMMAND ----------

# DBTITLE 1,Silver: texto plano directo + CSV a markdown
from pyspark.sql.functions import col, lit, decode, when, concat, expr

endpoint = "databricks-gpt-oss-20b"

# .md y .txt ya son texto legible: se decodifican directo, sin LLM.
# Solo el .csv se convierte a tabla markdown para facilitar el chunking.
csv_prompt = concat(
    lit("The following is the raw content of a CSV file. Convert it into a clean markdown table: "),
    lit("use the first row as the header and preserve every row and value exactly. "),
    lit("Output only the markdown table, with no explanations and no code fences.\n\nCSV:\n\n")
)

parsed_df = (bronze_df
              .withColumn("csv_prompt", csv_prompt)
              .withColumn("plain_text",
                          when(col("path").endswith(".csv"),
                               expr(f"""ai_query('{endpoint}',
                                                 CONCAT(csv_prompt, decode(content, 'UTF-8')),
                                                 responseFormat => '{{"type":"text"}}')"""))
                          .otherwise(decode(col("content"), "UTF-8")))
              .select("path", "plain_text")
            )

display(parsed_df)

# COMMAND ----------

# DBTITLE 1,Verificación del CSV convertido
# Verificación: el único documento convertido por el LLM debe ser el CSV,
# y debe salir como tabla markdown legible.
sample = parsed_df.filter(col("path").endswith(".csv")).collect()
print(sample[0]["path"])
print(sample[0]["plain_text"])

# COMMAND ----------

parsed_df.write.mode("overwrite").saveAsTable("silver_docs_parsed")