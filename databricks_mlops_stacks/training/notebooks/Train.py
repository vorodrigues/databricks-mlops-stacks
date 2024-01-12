# Databricks notebook source
##################################################################################
# Model Training Notebook
#
# This notebook shows an example of a Model Training pipeline using Delta tables.
# It is configured and can be executed as the "Train" task in the model_training_job workflow defined under
# ``databricks_mlops_stacks/assets/model-workflow-asset.yml``
#
# Parameters:
# * env (required):                 - Environment the notebook is run in (staging, or prod). Defaults to "staging".
# * training_data_path (required)   - Path to the training data.
# * experiment_name (required)      - MLflow experiment name for the training runs. Will be created if it doesn't exist.
# * model_name (required)           - Three-level name (<catalog>.<schema>.<model_name>) to register the trained model in Unity Catalog. 
#  
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
# DBTITLE 1, Notebook arguments

# List of input args needed to run this notebook as a job.
# Provide them via DB widgets or notebook arguments.

# Notebook Environment
dbutils.widgets.dropdown("env", "staging", ["staging", "prod"], "Environment Name")
env = dbutils.widgets.get("env")

# Path to the Hive-registered Delta table containing the training data.
dbutils.widgets.text(
    "training_data_path",
    "/databricks-datasets/nyctaxi-with-zipcodes/subsampled",
    label="Path to the training data",
)

# MLflow experiment name.
dbutils.widgets.text(
    "experiment_name",
    f"/dev-databricks-mlops-stacks-experiment",
    label="MLflow experiment name",
)
# Unity Catalog registered model name to use for the trained model.
dbutils.widgets.text(
    "model_name", "dev.vr_mlops_stacks.databricks-mlops-stacks-model", label="Full (Three-Level) Model Name"
)

# COMMAND ----------
# DBTITLE 1,Define input and output variables

input_table_path = dbutils.widgets.get("training_data_path")
experiment_name = dbutils.widgets.get("experiment_name")
model_name = dbutils.widgets.get("model_name")

# COMMAND ----------
# DBTITLE 1, Set experiment

import mlflow

mlflow.set_experiment(experiment_name)
mlflow.set_registry_uri('databricks-uc')

# COMMAND ----------
# DBTITLE 1, Load raw data

training_df = spark.read.format("delta").load(input_table_path)
training_df.display()

# COMMAND ----------
# DBTITLE 1, Helper function
from mlflow.tracking import MlflowClient
import mlflow.pyfunc


def get_latest_model_version(model_name):
    latest_version = 1
    mlflow_client = MlflowClient()
    for mv in mlflow_client.search_model_versions(f"name='{model_name}'"):
        version_int = int(mv.version)
        if version_int > latest_version:
            latest_version = version_int
    return latest_version


# COMMAND ----------

# MAGIC %md
# MAGIC Train a LightGBM model on the data, then log and register the model with MLflow.

# COMMAND ----------
# DBTITLE 1, Train model

import mlflow
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import mlflow.lightgbm

# Collect data into a Pandas array for training. Since the timestamp columns would likely
# cause the model to overfit the data, exclude them to avoid training on them.
columns = [col for col in training_df.columns if col not in ['tpep_pickup_datetime', 'tpep_dropoff_datetime']]
data = training_df.toPandas()[columns]

train, test = train_test_split(data, random_state=123)
X_train = train.drop(["fare_amount"], axis=1)
X_test = test.drop(["fare_amount"], axis=1)
y_train = train.fare_amount
y_test = test.fare_amount

mlflow.lightgbm.autolog()
train_lgb_dataset = lgb.Dataset(X_train, label=y_train.values)
test_lgb_dataset = lgb.Dataset(X_test, label=y_test.values)

param = {"num_leaves": 32, "objective": "regression", "metric": "rmse"}
num_rounds = 100

# Train a lightGBM model
model = lgb.train(param, train_lgb_dataset, num_rounds)

# COMMAND ----------
# DBTITLE 1, Log model and return output.

# Take the first row of the training dataset as the model input example.
input_example = X_train.iloc[[0]]

# Log the trained model with MLflow
mlflow.lightgbm.log_model(
    model, 
    artifact_path="lgb_model", 
    # The signature is automatically inferred from the input example and its predicted output.
    input_example=input_example,    
    registered_model_name=model_name
)

# The returned model URI is needed by the model deployment notebook.
model_version = get_latest_model_version(model_name)
model_uri = f"models:/{model_name}/{model_version}"
dbutils.jobs.taskValues.set("model_uri", model_uri)
dbutils.jobs.taskValues.set("model_name", model_name)
dbutils.jobs.taskValues.set("model_version", model_version)
dbutils.notebook.exit(model_uri)
