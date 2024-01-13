## Set up

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