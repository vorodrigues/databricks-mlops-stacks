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
    git commit -m init
    git push origin main
    git checkout -b dev
    ```







    - [Create PATs for dev, staging and prod Databricks Workspaces](https://docs.databricks.com/dev-tools/api/latest/authentication.html)
    - [Configure authentication credentials](https://docs.databricks.com/dev-tools/cli/index.html#connection-profiles)
    ```
    databricks configure --token --profile <dev-ws|staging-ws|prod-ws>
    ```



    - [Create a PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
1. Configure Databricks secrets for GitHub Actions
    - Within the GitHub project navigate to Secrets under the project settings
    - To run the GitHub actions workflows we require the following GitHub actions secrets:
        - `DATABRICKS_STAGING_HOST`
            - URL of Databricks staging workspace
        - `DATABRICKS_STAGING_TOKEN`
            - Databricks access token for staging workspace
        - `DATABRICKS_PROD_HOST`
            - URL of Databricks production workspace
        - `DATABRICKS_PROD_TOKEN`
            - Databricks access token for production workspace
        - `GH_TOKEN`
            - GitHub personal access token
1. Configure DBX
    - The project is designed to use 3 different profiles: dev, staging and prod. 
      These profiles are set in `.dbx/project.json`.
    - Note that for demo purposes we use the same connection profile for each of the 3 environments. 
      **In practice each profile would correspond to separate dev, staging and prod Databricks workspaces.**
    - This file will have to be adjusted accordingly to the connection profiles configured with Databricks CLI.
1. Customize project
    - .dbx/
        - project.json
    - .github/
        - workflows/
            - onpullrequest.yml
            - onrelease.yml
    - conf/
        - job_configs/
            - model_inference_batch.yml
            - model_train.yml
            - sample_test.yml
        - .dev.env
        - .staging.env
        - .prod.env
        - deployment.yml