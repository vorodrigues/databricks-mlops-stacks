"""This module contains utils shared between different notebooks"""

def get_deployed_model_stage_for_env(env):
    """
    Get the model version stage under which the latest deployed model version can be found
    for the current environment
    :param env: Current environment
    :return: Model version stage
    """
    # For a registered model version to be served, it needs to be in either the Staging or Production
    # model registry stage
    # (https://docs.databricks.com/applications/machine-learning/manage-model-lifecycle/index.html#transition-a-model-stage).
    # For models in dev and staging environments, we deploy the model to the "Staging" stage, and in prod we deploy to the
    # "Production" stage
    _MODEL_STAGE_FOR_ENV = {
        "dev": "Staging",
        "staging": "Staging",
        "prod": "Production",
        "test": "Production",
    }
    return _MODEL_STAGE_FOR_ENV[env]
