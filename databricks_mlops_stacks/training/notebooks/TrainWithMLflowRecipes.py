# Databricks notebook source
##################################################################################
# Model Training Notebook
##
# This notebook runs the MLflow Regression Recipe to train and registers an MLflow model in the model registry.
# It is configured and can be executed as the "Train" task in the model_training_job workflow defined under
# ``databricks_mlops_stacks/assets/model-workflow-asset.yml``
#
# NOTE: In general, we recommend that you do not modify this notebook directly, and instead update data-loading
# and model training logic in Python modules under the `steps` directory.
# Modifying this notebook can break model training CI/CD.
#
# However, if you do need to make changes (e.g. to remove the use of MLflow Recipes APIs),
# be sure to preserve the following interface expected by CI and the production model training job:
#
# Parameters:
#
# * env (optional): Name of the environment the notebook is run in (test, staging, or prod).
#                   You can add environment-specific logic to this notebook based on the value of this parameter,
#                   e.g. read training data from different tables or data sources across environments.
#                   The `databricks-dev` profile will be used if users manually run the notebook.
#                   The `databricks-test` profile will be used during CI test runs.
#                   This separates the potentially many runs/models logged during integration tests from
#                   runs/models produced by staging/production model training jobs. You can use the value of this
#                   parameter to further customize the behavior of this notebook based on whether it's running as
#                   a test or for recurring model training in staging/production.
#
#
# Return values:
# * model_uri: The notebook must return the URI of the registered model as notebook output specified through
#              dbutils.notebook.exit() AND as a task value with key "model_uri" specified through
#              dbutils.jobs.taskValues(...), for use by downstream notebooks.
#
# For details on MLflow Recipes and the individual split, transform, train etc steps below, including usage examples,
# see the Regression Recipe overview documentation: https://mlflow.org/docs/latest/recipes.html
# and Regression Recipes API documentation: https://mlflow.org/docs/latest/python_api/mlflow.recipes.html
##################################################################################

# COMMAND ----------
# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import os
notebook_path =  '/Workspace/' + os.path.dirname(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())
%cd $notebook_path

# COMMAND ----------

# MAGIC %pip install -r ../../requirements.txt

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import os
notebook_path =  '/Workspace/' + os.path.dirname(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get())
%cd $notebook_path
%cd ../

# COMMAND ----------

from mlflow.recipes import Recipe

try:
    # Profile from databricks workflow input will be used.
    env = dbutils.widgets.get("env")
    profile = f"databricks-{env}"
except:
    # When the users manually run the notebook, we use the "databricks-dev" profile instead of staging, prod or test.
    profile = "databricks-dev"

# COMMAND ----------

from mlflow.recipes.utils import (
    get_recipe_config,
    get_recipe_root_path,
)

root_path = get_recipe_root_path()
config = get_recipe_config(root_path, profile)
if config['experiment']['name'].startswith(f"/{env}-databricks-mlops-stacks-experiment"):
    print("WARNING: The experiment name may not have been set correctly. Please confirm that the experiment name in the profile YAML file matches the experiment_name variable in databricks_mlops_stacks/databricks.yml.")

# COMMAND ----------

r = Recipe(profile=profile)

# COMMAND ----------

r.clean()

# COMMAND ----------

r.inspect()

# COMMAND ----------

r.run("ingest")

# COMMAND ----------

r.run("split")

# COMMAND ----------

r.run("transform")

# COMMAND ----------

r.run("train")

# COMMAND ----------

r.run("evaluate")

# COMMAND ----------

r.run("register")

# COMMAND ----------

r.inspect("train")

# COMMAND ----------

test_data = r.get_artifact("test_data")
test_data.describe()

# COMMAND ----------

model_version = r.get_artifact("registered_model_version")
model_uri = f"models:/{model_version.name}/{model_version.version}"
dbutils.jobs.taskValues.set("model_uri", model_uri)
dbutils.jobs.taskValues.set("model_name", model_version.name)
dbutils.jobs.taskValues.set("model_version", model_version.version)
dbutils.notebook.exit(model_uri)
