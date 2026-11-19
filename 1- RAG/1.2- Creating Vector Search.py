# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %pip install --quiet --upgrade databricks-vectorsearch flashrank
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vs_client = VectorSearchClient(disable_notice=True)
vs_endpoint_name = "vs_endpoint"

if vs_client.endpoint_exists(vs_endpoint_name):
  vs_client.wait_for_endpoint(vs_endpoint_name)
else:
  vs_client.create_endpoint_and_wait(vs_endpoint_name, endpoint_type='STANDARD')

# COMMAND ----------

source_table_fullname = f"{project.catalog}.{project.schema}.gold_docs_chunked"

spark.sql(f"ALTER TABLE `{project.catalog}`.`{project.schema}`.gold_docs_chunked SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")

# COMMAND ----------

vs_index_fullname = f"{project.catalog}.{project.schema}.git_vs_index"

if not vs_client.index_exists(vs_endpoint_name, vs_index_fullname):
  vs_index = vs_client.create_delta_sync_index_and_wait(
    source_table_name=source_table_fullname,
    index_name=vs_index_fullname, 
    primary_key="id",
    embedding_source_column="chunk",
    embedding_model_endpoint_name="databricks-gte-large-en",
    endpoint_name=vs_endpoint_name,
    pipeline_type="TRIGGERED", # TRIGGERED or STREAMING
  )
else:
  vs_index = vs_client.get_index(vs_endpoint_name, vs_index_fullname)
  vs_index.wait_until_ready(wait_for_updates=True)

# COMMAND ----------

query_1 = "Explain the main git commands to initialize and clone a repository"
results = vs_index.similarity_search(
    query_text=query_1,
    columns=["path", "chunk"],
    num_results=3,
)

passages = results.get("result", {}).get("data_array", [])

display(passages)

# COMMAND ----------

query_2 = "Difference between git pull and git fetch"
results_fulltext = vs_index.similarity_search(
    query_text=query_2,
    columns=["path", "chunk"],
    query_type="FULL_TEXT",
    num_results=3
)

passages_fulltext = results_fulltext.get("result", {}).get("data_array", [])

display(passages_fulltext)

# COMMAND ----------

query_3 = "How do I resolve a merge conflict?"
results_hybrid = vs_index.similarity_search(
    query_text=query_3,
    columns=["path", "chunk"],
    query_type="hybrid",
    num_results=5
)

passages_hybrid = results_hybrid.get("result", {}).get("data_array", [])

display(passages_hybrid)

# COMMAND ----------

query_4 = "How do I undo the last commit but keep the changes?"
results_filtered = vs_index.similarity_search(
    query_text=query_4,
    columns=["path", "chunk"],
    filters={"path NOT" : f"dbfs:/Volumes/workspace/git-assistnat-agent/dataset/guias/01_comandos_fundamentales.md"},
    num_results=3
)

passages_filtered = results_filtered.get("result", {}).get("data_array", [])

display(passages_filtered)

# COMMAND ----------

from flashrank.Ranker import Ranker, RerankRequest

query_5 = "How do I configure SSH authentication for GitHub?"

ranker = Ranker()

results_initial = vs_index.similarity_search(
    query_text=query_5,
    columns=["path", "chunk"],
    num_results=10,
)

candidates = results_initial.get("result", {}).get("data_array", [])

rerank_request = RerankRequest(
    query=query_5,
    passages=[{"id": i, "text": row[1]} for i, row in enumerate(candidates)],
)

ranked = ranker.rerank(rerank_request)

reranked_passages = [candidates[r["id"]] for r in ranked[:4]]

display(reranked_passages)

# COMMAND ----------

from flashrank import Ranker, RerankRequest

cache_dir = f"{project.cache_volume}/flashrank"
ranker = Ranker(model_name="rank-T5-flan", cache_dir=cache_dir)

docs = [
    {"file": doc[0], "text": doc[1]}
    for doc in results.get("result", {}).get("data_array", [])
]

rerankrequest = RerankRequest(query=query_1, passages=docs)
passages_flashrank = ranker.rerank(rerankrequest)

formatted_output = [
    {"file": doc["file"], "text": doc["text"], "score": float(doc["score"])} 
    for doc in passages_flashrank
]

display(formatted_output)