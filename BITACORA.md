# Bitácora del Proyecto — Git Assistant Agent

**Proyecto:** Asistente RAG sobre documentación de Git
**Entorno:** Databricks (Unity Catalog + Delta Lake + Vector Search + MLflow)
**Repositorio:** `bootcamp-IA`
**Rama:** `main`
**Última actualización:** 2026-11-19
**Estado:** Fase 1 (RAG) y Fase 2 (AI Agents) completadas. Fase 3 (Evaluación) en curso.

---

## 1. Objetivo

Construir un asistente capaz de responder preguntas sobre Git usando como base de conocimiento un dataset propio de documentación (guías, matrices de situaciones y troubleshooting). El proyecto recorre el ciclo completo en Databricks:

1. Ingesta de documentos a un volumen de Unity Catalog.
2. Pipeline Medallion (Bronze → Silver → Gold) hasta chunks listos para búsqueda.
3. Índice de Vector Search para recuperación semántica.
4. Funciones de Unity Catalog y agente tool-calling registrado y desplegable.

---

## 2. Alcance de esta bitácora

Esta bitácora cubre lo trabajado hasta el momento:

- **Fase 1 — RAG:** preparación de datos y creación del índice vectorial.
- **Fase 2 — AI Agents:** funciones UC y agente tool-calling.

La Fase 3 (evaluación) queda documentada como trabajo pendiente.

---

## 3. Dataset

El dataset vive en el volumen:

```
/Volumes/workspace/git-assistnat-agent/dataset
```

| Carpeta | Contenido | Formato |
|---|---|---|
| `guias/` | 11 documentos de guías de Git (comandos, ramas, commits, SSH, tags, PRs, conflictos, seguridad, stash, aliases) | `.md` y `.txt` |
| `matrices/` | Recetario de situaciones comunes de Git | `.md` |
| `troubleshooting/` | Errores de terminal y sus soluciones | `.csv` |

Total: 13 archivos.

---

## 4. Arquitectura del pipeline

```
Volumen UC (dataset)
        │
        ▼
1.1A Bronze  →  bronze_docs_raw        (binario + ingestion_time)
        │
        ▼
1.1B Silver  →  silver_docs_parsed     (texto plano; CSV → markdown)
        │
        ▼
1.1C Gold    →  gold_docs_chunked      (chunks + id)
        │
        ▼
1.2 Vector Search  →  git_vs_index     (Delta Sync Index + embeddings)
        │
        ▼
2.3 UC Functions  →  search_git_docs, get_current_user, build_reference
        │
        ▼
2.4 Agente tool-calling  →  git_agent  (MLflow + UC + Vector Search)
```

Infraestructura común: `Includes/Lab_Setup.ipynb` define `ProjectSetup`, que fija catálogo, schema, volumen del dataset, `_cache` y `_checkpoint`.

---

## 5. Fase 1 — RAG

### 5.1 Bronze — `1.1A- Data Prep (Bronze).py`

- Lee las tres carpetas del dataset (`guias`, `matrices`, `troubleshooting`) con `spark.read.format("binaryfile")`.
- Agrega `ingestion_time` con `current_timestamp()`.
- Persiste en la tabla **`bronze_docs_raw`**.

Decisión: leer las tres carpetas en lugar de una sola, para que el índice cubra también matrices y troubleshooting.

### 5.2 Silver — `1.1B- Data Prep (Silver).py`

- Los archivos `.md` y `.txt` ya son texto: se decodifican directamente con `decode(content, 'UTF-8')`, sin LLM.
- El `.csv` se convierte a tabla markdown con `ai_query` usando el endpoint `databricks-gpt-oss-20b`.
- Resultado: tabla **`silver_docs_parsed`** con `path` y `plain_text`.
- Incluye una celda de verificación del CSV convertido.

Decisión: no usar `ai_parse_document` para markdown/texto, porque el dataset no son PDFs y el parseo estructurado no aporta valor.

### 5.3 Gold — `1.1C- Data Prep (Gold).py`

- Chunking con `RecursiveCharacterTextSplitter`:
  - `chunk_size = 1500`
  - `chunk_overlap = 150`
  - separadores: `== page ==`, doble salto, salto, espacio y vacío.
- Chunking distribuido con `pandas_udf` + `explode`.
- Agrega `id` con `monotonically_increasing_id()`.
- Persiste en la tabla **`gold_docs_chunked`** con `path`, `chunk` e `id`.

### 5.4 Vector Search — `1.2- Creating Vector Search.py`

- Endpoint: **`vs_endpoint`** (tipo `STANDARD`), creado si no existe.
- Habilita Change Data Feed en `gold_docs_chunked`.
- Índice Delta Sync: **`git_vs_index`**.
  - `primary_key = "id"`
  - `embedding_source_column = "chunk"`
  - `embedding_model_endpoint_name = "databricks-gte-large-en"`
  - `pipeline_type = "TRIGGERED"`
- Pruebas incluidas:
  - búsqueda semántica,
  - búsqueda full-text,
  - búsqueda híbrida,
  - búsqueda con filtro por `path`,
  - reranking con `flashrank`.

---

## 6. Fase 2 — AI Agents

### 6.1 UC Functions — `2.3- Agents with UC Functions.py`

Funciones creadas en `git-assistnat-agent`:

| Función | Tipo | Descripción |
|---|---|---|
| `search_git_docs(search_term STRING)` | SQL | Busca chunks de la documentación Git por término y devuelve `path` y `chunk`. |
| `get_current_user()` | SQL | Devuelve el usuario de la sesión. |
| `build_reference(path, chunk)` | Python UC | Arma una referencia corta con el nombre de archivo y los primeros 200 caracteres del chunk. |

Todas se apoyan en la tabla `gold_docs_chunked` y en `project.catalog` / `project.schema`.

### 6.2 Agente tool-calling — `2.4- driver (git_agent).py`

- Implementa un `ToolCallingAgent` basado en `mlflow.pyfunc.ResponsesAgent`.
- Herramientas:
  - funciones UC de `workspace.git-assistnat-agent.*`,
  - `VectorSearchRetrieverTool` sobre `workspace.git-assistnat-agent.git_vs_index`.
- LLM: `databricks-gpt-oss-120b`.
- System prompt orientado a Git.
- Incluye pruebas manuales (`predict` y `predict_stream`), logging del modelo, validación pre-despliegue, registro como **`git_agent`** y despliegue con `agents.deploy`.

### 6.3 Registro y despliegue

- Modelo registrado en Unity Catalog como `git_agent`.
- Despliegue configurado con `scale_to_zero=True`.

---

## 7. Decisiones de diseño

1. **Adaptación del dataset:** el material original era de un curso con ejemplos de teléfonos. Se reemplazó por documentación de Git y se eliminaron todas las referencias al dominio anterior (tablas `smartphones`/`inventory_stock`, agente `dphone_agent`, índice `dphone_vs_index`, preguntas y guidelines de ejemplo).
2. **Schema único `git-assistnat-agent`:** tablas, funciones, caché y checkpoints viven en el mismo schema que el volumen del dataset.
3. **Identificadores con guiones:** como el schema contiene guiones, todo SQL usa backticks (`` `git-assistnat-agent` ``). Ejemplo: `ALTER TABLE \`workspace\`.\`git-assistnat-agent\`.gold_docs_chunked ...`.
4. **`dataset_volume` explícito:** no se deriva del schema; se fija a `/Volumes/workspace/git-assistnat-agent/dataset`.
5. **Sin descarga desde S3:** se eliminó `download_dataset`; el dataset ya está en el volumen.
6. **Silver sin `ai_parse_document`:** markdown y texto se decodifican directo; solo el CSV pasa por LLM.
7. **Chunking por páginas:** los separadores respetan `== page ==` para conservar la estructura de los documentos.

---

## 8. Problemas encontrados y soluciones

| Problema | Causa | Solución |
|---|---|---|
| Rutas y ejemplos de teléfonos | Material original de otro curso | Dataset y contenido reemplazados por Git |
| Faltaba `Includes/` | `%run ../Includes/Lab_Setup` no resolvía | Se creó `Includes/` y se movió `Lab_Setup.ipynb` |
| `Lab_Setup_02` inexistente | Referencia rota en `2.3` | Se cambió a `../Includes/Lab_Setup` |
| `ai_parse_document` no aplicaba | El dataset es `.md`/`.txt`/`.csv`, no PDFs | Decodificación UTF-8 directa; CSV a markdown con `ai_query` |
| SQL fallaba con el schema | El nombre `git-assistnat-agent` tiene guiones | Backticks en todos los identificadores SQL |
| Tablas `raw/*.csv` inexistentes | Se arrastraban del dataset anterior | Se eliminaron `create_agent_tables` y `create_batch_tables` |
| Descarga S3 redundante | El dataset ya estaba en el volumen | Se eliminó `download_dataset` y el parámetro `uri` |
| Modelo/índice con nombres de teléfonos | Restos del curso | Renombrados a `git_agent` y `git_vs_index` |

---

## 9. Estado actual y próximos pasos

### Completado

- [x] Estructura de proyecto y `Lab_Setup`.
- [x] Pipeline Bronze → Silver → Gold.
- [x] Índice `git_vs_index` y pruebas de búsqueda.
- [x] Funciones UC (`search_git_docs`, `get_current_user`, `build_reference`).
- [x] Agente tool-calling `git_agent` con registro y despliegue configurados.

### Pendiente

- [ ] Ejecución end-to-end documentada con evidencias (capturas/tablas).
- [ ] Cierre de Fase 3: evaluación con `mlflow.genai.evaluate` y guidelines de Git.
- [x] `README.md` actualizado con arquitectura, dataset y guía de ejecución.
- [ ] Entrega final.

---

## 10. Evidencia de commits

| Commit | Fecha | Descripción |
|---|---|---|
| `c404a78` | 2026-11-19 | Fix de errores tras pruebas en Databricks |
| `c6535aa` | 2026-11-19 | Refactor del agente Git: modelo, evaluación y tool-calling |
| `ba0dc96` | 2026-11-19 | Guías de Git: SSH, tags, PRs, conflictos, seguridad, stash, aliases |
| `a55df52` | 2026-11-19 | Guías de Git y troubleshooting |
