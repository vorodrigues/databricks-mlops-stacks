# ML Developer Guide using MLflow Recipes

[(back to main README)](../../README.md)

## Table of contents
* [Initial setup](#initial-setup): adapting the provided example code to your ML problem
* [Iterating on ML code](#iterating-on-ml-code): making and testing ML code changes on Databricks or your local machine.
* [Next steps](#next-steps)

## Initial setup
This folder contains example ML code to train a regression model to predict NYC taxi fares using
[MLflow recipes](https://mlflow.org/docs/latest/recipes.html).

**Note**: MLflow Recipes currently supports regression and classification problems. Usage of MLflow Recipes is encouraged but not required: you can still use the provided
CI/CD and ML asset configs to build production ML pipelines, as long as you provide ML notebooks  under `notebooks` 
directory of the corresponding component, for example, model training notebooks in `databricks_mlops_stacks/training/notebooks`, 
batch inference notebook in `databricks_mlops_stacks/deployment/batch_inference/notebooks`.
See code comments in files under `notebooks` for the expected interface & behavior of these notebooks.

If you're not using MLflow Recipes, you can still follow the docs below to develop your ML code, skipping sections
that are targeted at MLflow Recipes users. Then, when you're ready
to productionize your ML project, ask your ops team to set up CI/CD and deploy
production jobs per the [MLOps setup guide](../../docs/mlops-setup.md).

### Configure your ML pipeline
**This section assumes use of MLflow Recipes**.

Address TODOs in the recipe configs under `databricks_mlops_stacks/training/recipe.yaml`, `databricks_mlops_stacks/training/profiles/databricks-dev.yaml`,
and `databricks_mlops_stacks/training/profiles/local.yaml`, specifying configs such as the training dataset path(s) to use when developing
locally or on Databricks.

For details on the meaning of recipe configurations, see the comments in [this example recipe.yaml](https://github.com/mlflow/recipes-regression-template/blob/main/recipe.yaml).
The purpose and behavior of the individual recipe steps (`ingest`, `train`, etc) being configured are also
described in detail in
the [Recipe overview](https://mlflow.org/docs/latest/recipes.html)
and [API documentation](https://mlflow.org/docs/latest/python_api/mlflow.recipes.html).

After configuring your recipe, you can iterate on and test ML code under ``databricks_mlops_stacks/training/steps``.
We expect most development to take place in the abovementioned YAML config files and
`databricks_mlops_stacks/training/steps/train.py` (model training logic).

## Iterating on ML code

### Deploy ML code and assets to dev workspace using Bundles

Refer to [Local development and dev workspace](../assets/README.md#local-development-and-dev-workspace)
to use databricks CLI bundles to deploy ML code together with ML asset configs to dev workspace. 

### Develop on Databricks using Databricks Repos

#### Prerequisites
You'll need:
* Access to run commands on a cluster running Databricks Runtime ML version 11.0 or above in your dev Databricks workspace
* To set up [Databricks Repos](https://docs.databricks.com/repos/index.html): see instructions below

#### Configuring Databricks Repos
To use Repos, [set up git integration](https://docs.databricks.com/repos/repos-setup.html) in your dev workspace.

If the current project has already been pushed to a hosted Git repo, follow the
[UI workflow](https://docs.databricks.com/repos/git-operations-with-repos.html#add-a-repo-connected-to-a-remote-repo)
to clone it into your dev workspace and iterate.

Otherwise, e.g. if iterating on ML code for a new project, follow the steps below:
* Follow the [UI workflow](https://docs.databricks.com/repos/git-operations-with-repos.html#add-a-repo-connected-to-a-remote-repo)
  for creating a repo, but uncheck the "Create repo by cloning a Git repository" checkbox.
* Install the `dbx` CLI via `pip install --upgrade dbx`
* Run `databricks configure --profile databricks-mlops-stacks-dev --token --host <your-dev-workspace-url>`, passing the URL of your dev workspace.
  This should prompt you to enter an API token
* [Create a personal access token](https://docs.databricks.com/dev-tools/auth.html#personal-access-tokens-for-users)
  in your dev workspace and paste it into the prompt from the previous step
* From within the root directory of the current project, use the [dbx sync](https://dbx.readthedocs.io/en/latest/guides/python/devloop/mixed/#using-dbx-sync-repo-for-local-to-repo-synchronization) tool to copy code files from your local machine into the Repo by running
  `dbx sync repo --profile databricks-mlops-stacks-dev --source . --dest-repo your-repo-name`, where `your-repo-name` should be the last segment of the full repo name (`/Repos/username/your-repo-name`)

#### Running code on Databricks
You can iterate on ML code by running the provided `databricks_mlops_stacks/training/notebooks/TrainWithMLflowRecipes.py` notebook on Databricks using
[Repos](https://docs.databricks.com/repos/index.html). This notebook drives execution of
the ML code defined under ``databricks_mlops_stacks/training/steps``. You can use multiple browser tabs to edit
logic in `steps` and run the training recipe in the `TrainWithMLflowRecipes.py` notebook.


### Develop locally
**Note: this section assumes use of MLflow Recipes**.

You can also iterate on ML code locally.

#### Prerequisites
* Python 3.8+
* Install model training and test dependencies via `pip install -I -r databricks_mlops_stacks/requirements.txt -r test-requirements.txt` from project root directory.

#### Trigger model training
Run `mlp run --profile local` to trigger training locally. See the
[MLflow recipes CLI docs](https://mlflow.org/docs/latest/recipes.html#key-concepts) for details.

#### Inspect results in the UI
To facilitate saving and sharing results from local iteration with collaborators, we recommend configuring your
environment to log to a Databricks MLflow tracking server, as described in [this guide](https://docs.databricks.com/mlflow/access-hosted-tracking-server.html).
Then, update `profiles/local.yaml` to use a Databricks tracking URI,
e.g. `databricks://<profile-name>` instead of a local `sqlite://` URI. You can then easily view model training results in the Databricks UI.

If you prefer to log results locally (the default), you can view model training results by running the MLflow UI:

```sh
mlflow ui \
   --backend-store-uri sqlite:///mlruns.db \
   --default-artifact-root ./mlruns \
   --host localhost
```

Then, open a browser tab pointing to [http://127.0.0.1:5000](http://127.0.0.1:5000)

#### Run unit tests
You can run unit tests for your ML code via `pytest tests`.

## Next Steps
If you're iterating on ML code for an existing, already-deployed ML project, follow [Submitting a Pull Request](../../docs/ml-pull-request.md)
to submit your code for testing and production deployment.

Otherwise, if exploring a new ML problem and satisfied with the results (e.g. you were able to train
a model with reasonable performance on your dataset), you may be ready to productionize your pipeline.
To do this, follow the [MLOps Setup Guide](../../docs/mlops-setup.md) to set up CI/CD and deploy
production training/inference pipelines.

[(back to main README)](../../README.md)
