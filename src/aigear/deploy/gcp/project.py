from ...common.logger import logger
from ...common.sh import run_sh


def get_project_id():
    project_id = None
    command = [
        "gcloud", "config", "get-value", "project"
    ]
    event = run_sh(command)
    if "unset" in event:
        logger.info("No project id set.")
    elif "ERROR" in event:
        logger.info(event)
    else:
        project_id = event.strip()
    return project_id


def get_region():
    region = None
    command = [
        "gcloud", "config", "get-value", "compute/region"
    ]
    event = run_sh(command)
    if "unset" in event:
        logger.info("No project id set.")
    elif "ERROR" in event:
        logger.info(event)
    else:
        region = event.strip()
    return region
