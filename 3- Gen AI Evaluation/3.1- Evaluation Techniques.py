# Databricks notebook source
# MAGIC %pip install --quiet --upgrade backoff databricks-openai uv databricks-agents mlflow-skinny[databricks]
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ../Includes/Lab_Setup

# COMMAND ----------

import mlflow

model_name = f"{project.catalog}.{project.schema}.git_agent"
model_version = 1
logged_model_uri = f"models:/{model_name}/{model_version}"

loaded_model = mlflow.pyfunc.load_model(logged_model_uri)

# COMMAND ----------

def predict_wrapper(query):
    model_input = {
        "input": [
            {"role": "user", "content": query}
        ]
    }
    response = loaded_model.predict(model_input)

    return response["output"][-1]["content"][0]["text"]

# COMMAND ----------

predict_wrapper("How do I undo the last commit but keep the changes?")

# COMMAND ----------

eval_dataset = [
    {
        "inputs": {'query': 'How do I resolve a merge conflict?'},
        "expectations": None
    },
    {
        "inputs": {'query': 'What is the difference between git merge and git rebase?'},
        "expectations": None
    }
]

# COMMAND ----------

# MAGIC %md
# MAGIC ![llm-judges.png](../Includes/Images/llm-judges.png "LLM Judges")

# COMMAND ----------

from mlflow.genai.scorers import RelevanceToQuery, RetrievalRelevance, RetrievalGroundedness, Safety

eval_results = mlflow.genai.evaluate(
    predict_fn=predict_wrapper,
    data=eval_dataset,
    scorers=[RelevanceToQuery(), RetrievalRelevance(), RetrievalGroundedness(), Safety()],
)

# COMMAND ----------

eval_dataset_with_facts = [
    {
        "inputs": {'query': 'Which git commands are used to save work temporarily?'},
        "expectations":  {"expected_facts": ["git stash push", "git stash pop"]}
    },
    {
        "inputs": {'query': 'What does git status show?'},
        "expectations": {'expected_response': 'modified files, untracked files, and staged files'}
    }
]

# COMMAND ----------

# MAGIC %md
# MAGIC ![llm-judges.png](../Includes/Images/llm-judges-with-ground-truth.png "LLM Judges")

# COMMAND ----------

from mlflow.genai.scorers import Correctness, RetrievalSufficiency

eval_results = mlflow.genai.evaluate(
    data=eval_dataset_with_facts,
    predict_fn=predict_wrapper,
    scorers=[RelevanceToQuery(), RetrievalRelevance(), RetrievalGroundedness(), Safety(),
             Correctness(), RetrievalSufficiency()],
)

# COMMAND ----------

from mlflow.genai.scorers import Guidelines

english_guidelines = Guidelines(
    name="english",
    guidelines=["The response must be in English"]
)

tone_guidelines = Guidelines(
    name="professional_tone",
    guidelines=["""The response must:
                    - maintain formal, respectful, and empathetic tone"
                    - avoid slang, casual expressions, or humor"""]
)

compliance_guidelines = Guidelines(
    name="git_accuracy",
    guidelines=[
        """Accuracy:
        - The response must be based on the provided Git documentation
        - The response must not invent commands or flags that do not exist in Git
        - The response must warn the user before recommending destructive commands""",

        """Safety:
        - The response must never ask for passwords, tokens, or SSH private keys
        - The response must not encourage committing secrets to a repository""",

        """Scope:
        - The response must stay focused on Git and version control topics
        - The response must not answer unrelated questions"""
    ],
    model="databricks:/databricks-gpt-oss-120b"
)

# COMMAND ----------

eval_results = mlflow.genai.evaluate(
    data=eval_dataset_with_facts,
    predict_fn=predict_wrapper,
    scorers=[RelevanceToQuery(), RetrievalRelevance(), RetrievalGroundedness(), Safety(),
             Correctness(), RetrievalSufficiency(),
             english_guidelines, tone_guidelines, compliance_guidelines],
)

# COMMAND ----------

eval_results

# COMMAND ----------

eval_results.result_df

# COMMAND ----------

model_name = f"{project.catalog}.{project.schema}.git_agent"
#model_version = 2
#logged_model_uri = f"models:/{model_name}/{model_version}"
model_alias = "challenger"
logged_model_uri = f"models:/{model_name}@{model_alias}"

challenger_model = mlflow.pyfunc.load_model(logged_model_uri)

# COMMAND ----------

def challenger_predict_wrapper(query):
    model_input = {
        "input": [
            {"role": "user", "content": query}
        ]
    }
    response = challenger_model.predict(model_input)

    for item in reversed(response["output"]):
        if item.get("type") == "message":
            if "content" in item:
                for content_item in item["content"]:
                    if content_item.get("type") == "output_text":
                        return content_item["text"]
    
    return None

challenger_results = mlflow.genai.evaluate(
    predict_fn=challenger_predict_wrapper,
    data=eval_dataset_with_facts,
    scorers=[RelevanceToQuery(), RetrievalRelevance(), RetrievalGroundedness(), Safety(),
             Correctness(), RetrievalSufficiency(),
             english_guidelines, tone_guidelines, compliance_guidelines],
)