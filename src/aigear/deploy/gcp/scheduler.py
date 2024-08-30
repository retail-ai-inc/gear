import json
from ...common.logger import logger
from ...common.sh import run_sh


class Scheduler:
    def __init__(
        self,
        name: str,
        location: str,
        schedule: str,
        topic_name: str,
        message: any,
        time_zone: str = "Etc/UTC",
    ):
        self.name = name
        self.location = location
        self.schedule = schedule
        self.topic_name = topic_name
        self.message = message
        self.time_zone = time_zone
    
    def create(self):
        is_exist = self.describe()
        if not is_exist:
            message_body = json.dumps(self.message)
            command = [
                "gcloud", "scheduler", "jobs", "create", "pubsub",
                self.name,
                "--location", self.location,
                "--schedule", self.schedule,
                "--topic", self.topic_name,
                "--message-body", message_body,
                "--time-zone", self.time_zone,
            ]
            event = run_sh(command)
            logger.info(event)
            if "ERROR" in event:
                logger.info("Error occurred while creating cloud function.")
        else:
            logger.info(f"the cloud scheduler(self.name) already exists.")
    
    def delete(self):
        command = [
            "gcloud", "scheduler", "jobs", "delete",
            self.name,
            "--location", self.location,
        ]
        event = run_sh(command, "yes\n")
        logger.info(event)
    
    def describe(self):
        is_exist = False
        command = [
            "gcloud", "scheduler", "jobs", "describe",
            self.name,
            "--location", self.location,
        ]
        event = run_sh(command)
        logger.info(event)
        if "ENABLED" in event:
            is_exist = True
        return is_exist
    
    def list(self):
        command = [
            "gcloud", "scheduler", "jobs", "list",
            "--location", self.location,
            f"--filter={self.name}",
        ]
        event = run_sh(command)
        logger.info(f"\n{event}")
    
    def run(self):
        command = [
            "gcloud", "scheduler", "jobs", "run",
            self.name,
            "--location", self.location,
        ]
        event = run_sh(command)
        if event:
            logger.info(event)
        else:
            logger.info("Running successfully, executing job.")
    
    def pause(self):
        command = [
            "gcloud", "scheduler", "jobs", "pause",
            self.name,
            "--location", self.location,
        ]
        event = run_sh(command)
        logger.info(event)
    
    def resume(self):
        command = [
            "gcloud", "scheduler", "jobs", "resume",
            self.name,
            "--location", self.location,
        ]
        event = run_sh(command)
        logger.info(event)
    
    @staticmethod
    def update(
        name,
        location,
        schedule,
        topic_name,
        message,
    ):
        message_body = json.dumps(message)
        command = [
            "gcloud", "scheduler", "jobs", "update", "pubsub",
            name,
            "--location", location,
            "--schedule", schedule,
            "--topic", topic_name,
            "--message-body", message_body,
        ]
        event = run_sh(command)
        logger.info(event)
        if "ERROR" in event:
            logger.info("Error occurred while creating cloud function.")
