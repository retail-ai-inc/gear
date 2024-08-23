from ...common.logger import logger
from ...common.sh import run_sh


class PubSub:
    def __init__(self, topic_name: str):
        self.topic_name = topic_name
    
    def create(self):
        command = [
            "gcloud", "pubsub", "topics", "create", self.topic_name
        ]
        event = run_sh(command)
        logger.info(event)
    
    def describe(self):
        is_exist = False
        command = [
            "gcloud", "pubsub", "topics", "describe", self.topic_name
        ]
        event = run_sh(command)
        if "name: projects" in event:
            is_exist = True
            logger.info(f"Find resources: {event}")
        elif "NOT_FOUND" in event:
            logger.info(f"NOT_FOUND: Resource not found (resource={self.topic_name})")
        else:
            logger.info(event)
        return is_exist
    
    def delete(self):
        command = [
            "gcloud", "pubsub", "topics", "delete", self.topic_name
        ]
        event = run_sh(command)
        logger.info(event)
    
    def list(self):
        command = [
            "gcloud", "pubsub", "topics", "list", f"--filter=name.scope(topic):{self.topic_name}"
        ]
        event = run_sh(command)
        logger.info(event)
    
    def publish(self, message):
        command = [
            "gcloud", "pubsub", "topics", "publish", self.topic_name,
            f"--message = {message}",
        ]
        event = run_sh(command)
        logger.info(event)
