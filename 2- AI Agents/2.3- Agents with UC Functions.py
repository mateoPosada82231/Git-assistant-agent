# Databricks notebook source
# MAGIC %pip install --quiet --upgrade unitycatalog-ai
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT path, chunk
# MAGIC FROM gold_docs_chunked
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION search_git_docs(search_term STRING COMMENT 'Term to search in the Git documentation (string)')
# MAGIC RETURNS TABLE(path STRING, chunk STRING)
# MAGIC COMMENT 'Searches the Git documentation chunks for a given term and returns the matching file and text. IMPORTANT: This function accepts exactly one string parameter.'
# MAGIC RETURN
# MAGIC   SELECT path, chunk
# MAGIC   FROM gold_docs_chunked
# MAGIC   WHERE lower(chunk) LIKE concat('%', lower(search_term), '%')
# MAGIC   LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM search_git_docs('merge conflict')

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION get_current_user()
# MAGIC RETURNS STRING
# MAGIC COMMENT 'Returns the current session user, used for identifying the active user. IMPORTANT: This function accepts ZERO parameters. Do not pass any arguments.'
# MAGIC RETURN current_user();

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT get_current_user()

# COMMAND ----------

def build_reference(path: str, chunk: str) -> str:
    """
    Returns a short reference string for a Git documentation chunk.

    Args:
        path (str): Path of the documentation file inside the dataset volume.
        chunk (str): Text chunk retrieved from the documentation.

    Returns:
        str: Reference with the file name and the first 200 characters of the chunk.
    """
    file_name = path.rsplit("/", 1)[-1]
    return f"{file_name}: {chunk[:200]}"

# COMMAND ----------

build_reference(
    "/Volumes/workspace/git-assistnat-agent/dataset/guias/01_comandos_fundamentales.md",
    "git status muestra el estado de los archivos modificados, sin seguimiento y en staging.",
)

# COMMAND ----------

from unitycatalog.ai.core.databricks import DatabricksFunctionClient

client = DatabricksFunctionClient()

python_tool_uc_info = client.create_python_function(func=build_reference,
                                                    catalog=project.catalog,
                                                    schema=project.schema,
                                                    replace=True)
