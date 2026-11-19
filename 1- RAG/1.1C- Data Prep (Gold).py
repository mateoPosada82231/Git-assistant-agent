# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %pip install --quiet --upgrade langchain_text_splitters
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

silver_df = spark.read.table("silver_docs_parsed")
display(silver_df)

# COMMAND ----------

from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n== page ==\n", "== page ==", "\n\n", "\n", " ", ""]
)

def chunk_text(text):
    chunks = []
    if isinstance(text, str) and text.strip():
        for c in splitter.split_text(text):
            if c and c.strip():
                chunks.append(c)
    return chunks

# COMMAND ----------

doc = """# Comandos Fundamentales de Git

## Inicialización y Clonación

- **Iniciar un repositorio local nuevo:**
  ```bash
  git init
  ```
  Crea la carpeta oculta `.git` en el directorio actual para comenzar el seguimiento de versiones.

- **Clonar un repositorio remoto existente:**
  ```bash
  git clone <url_del_repositorio>
  ```
  Descarga el proyecto completo junto con todo su historial de commits y configura el remoto `origin`.

== page ==

## Ciclo Básico de Trabajo (Working Directory -> Staging -> Repositorio)

- **Revisar el estado de los archivos:**
  ```bash
  git status
  ```
  Muestra archivos modificados, archivos nuevos sin seguimiento (_untracked_) y archivos listos en el área de preparación (_staging area_).

- **Agregar archivos al área de preparación (Staging):**
  ```bash
  git add <nombre_archivo>
  git add .
  ```
  Usa `git add <archivo>` para incluir cambios específicos o `git add .` para preparar todos los cambios del directorio actual.

- **Guardar cambios en el historial (Commit):**
  ```bash
  git commit -m "feat: agregar validacion de usuario"
  ```
  Crea una instantánea permanente de los archivos que están en _staging_.

== page ==

## Sincronización con Repositorios Remotos

- **Descargar e integrar cambios de la rama remota actual:**
  ```bash
  git pull origin <nombre_rama>
  ```
  Equivale a ejecutar `git fetch` seguido de `git merge`.

- **Subir tus commits locales al repositorio remoto:**
  ```bash
  git push -u origin <nombre_rama>
  ```
"""
chunks = chunk_text(doc)
print(f'Number of chunks: {len(chunks)}')
chunks

# COMMAND ----------

from typing import Iterator
from pyspark.sql.functions import pandas_udf, explode
import pandas as pd

@pandas_udf("array<string>")
def get_chunks(batch_iter: Iterator[pd.Series]) -> Iterator[pd.Series]:
    for s in batch_iter:
        yield s.apply(chunk_text)

df_chunks = (silver_df.withColumn("chunk", explode(get_chunks("plain_text")))
                                        .select("path", "chunk")

            )

display(df_chunks)

# COMMAND ----------

from pyspark.sql.functions import monotonically_increasing_id

df_chunks = df_chunks.withColumn("id", monotonically_increasing_id())

df_chunks.write.mode("overwrite").saveAsTable("gold_docs_chunked")