# Databricks MLOps Stacks

> **_NOTE:_**  This feature is in [public preview](https://docs.databricks.com/release-notes/release-types.html).

This repo provides a customizable stack for starting new ML projects
on Databricks that follow production best-practices out of the box.

Using Databricks MLOps Stacks, data scientists can quickly get started iterating on ML code for new projects while ops engineers set up CI/CD and ML assets
management, with an easy transition to production. You can also use MLOps Stacks as a building block in automation for creating new data science projects with production-grade CI/CD pre-configured.

An ML solution comprises data, code, and models. These assets need to be developed, validated (staging), and deployed (production). In this repository, we use the notion of dev, staging, and prod to represent the execution
environments of each stage. 

An instantiated project from MLOps Stacks contains an ML pipeline with CI/CD workflows to test and deploy automated model training and batch inference jobs across your dev, staging, and prod Databricks workspaces. 

<img src="doc-images/mlops-stack-summary.png">

Data scientists can iterate on ML code and file pull requests (PRs). This will trigger unit tests and integration tests in an isolated staging Databricks workspace. Model training and batch inference jobs in staging will immediately update to run the latest code when a PR is merged into main. After merging a PR into main, you can cut a new release branch as part of your regularly scheduled release process to promote ML code changes to production.

---

# Process

---

# Set up

1. Install Python from https://www.anaconda.com (3.8+ / tested on 3.9.12)

1. Setup Databricks CLI (v0.211.0+ / tested on v0.212.0)
    - Install
    ```
    brew tap databricks/tap
    brew install databricks
    ```

1. [Setup your IDE of choice](https://docs.databricks.com/dev-tools/dbx.html#visual-studio-code)
    - For VS Code:
        - Install from https://code.visualstudio.com/download
        - Install Python extension from https://marketplace.visualstudio.com/items?itemName=ms-python.python
        - Create a directory for your project
        - Create a new Pipenv from the project directory
        ```
        pipenv --python <version>
        ```
        - Select the project Python interpreter

1. Setup MLOps Stacks project
    - Init project
    `databricks bundle init mlops-stacks`
    - Follow on-screen instructions

1. Setup GitHub repository
    - Create a new remote repository
    - Rename `master` branch to `main`
    - Install GIT from https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    - Initialize your local repository from the project directory
    ```
    git init
    git remote add origin <url>
    git config user.name <user.name>
    git config user.email <user.email>
    git add *
    git add .github/*
    git commit -m init
    git push origin main
    git checkout -b dev
    ```
    - [Generate Databricks PATs for STG and PRD environments](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    - [Generate GitHub PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    - Within the GitHub repository navigate to Settings > Secrets and variables > Actions
    - To run the GitHub actions workflows we require the following GitHub actions secrets:
        - `STAGING_WORKSPACE_TOKEN`
        - `PROD_WORKSPACE_TOKEN`
        - `GH_TOKEN`