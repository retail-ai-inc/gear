from ...common.logger import logger
from ...common.sh import run_sh


def check_iam(project_id: str):
    is_owner = False
    command = [
        "gcloud", "projects", "get-iam-policy",
        project_id,
        "--flatten=bindings[].members",
        "--format=table(bindings.role)",
        "--filter=bindings.members:$(gcloud config get-value account)",
    ]
    event = run_sh(command)
    if "roles/owner" in event:
        is_owner = True
    elif event == "":
        logger.info("The currently logged in GCP account does not have owner privileges.")
    else:
        logger.info(event)
    return is_owner
