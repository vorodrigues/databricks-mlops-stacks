# ML Developer Guide

[(back to main README)](../README.md)

## Table of contents
* [Iterating on ML code](#iterating-on-ml-code): making and testing ML code changes on Databricks or your local machine.
* [Next steps](#next-steps)

## Iterating on ML code

### Deploy ML code and assets to dev workspace using bundles

Refer to [Local development and dev workspace](../databricks_mlops_stacks/assets/README.md#local-development-and-dev-workspace) 
to use databricks CLI bundles to deploy ML code together with asset configs to the dev workspace.

This will allow you to develop locally and use databricks CLI bundles to deploy to your dev workspace to test out code and config changes.

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
You can iterate on the sample ML code by running the provided `databricks_mlops_stacks/training/notebooks/Train.py` notebook on Databricks using
[Repos](https://docs.databricks.com/repos/index.html). 


## Next Steps
If you're iterating on ML code for an existing, already-deployed ML project, follow [Submitting a Pull Request](ml-pull-request.md)
to submit your code for testing and production deployment.

Otherwise, if exploring a new ML problem and satisfied with the results (e.g. you were able to train
a model with reasonable performance on your dataset), you may be ready to productionize your pipeline.
To do this, follow the [MLOps Setup Guide](mlops-setup.md) to set up CI/CD and deploy
production training/inference pipelines.

[(back to main README)](../README.md)
