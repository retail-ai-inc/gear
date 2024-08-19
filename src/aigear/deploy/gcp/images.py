import subprocess
from ..docker.client import docker_client, ImageNotFound
from ...common.logger import logger


class ArtifactRegistry:
    def __init__(self):
        self.rep_exists = True
    
    def create(
        self,
        repository: str,
        location: str,
        description: str,
    ):
        command = [
            "gcloud", "artifacts", "repositories", "create", repository,
            "--repository-format=docker",
            f"--location={location}",
            f"--description={description}"
        ]
        self.run_sh(
            command=command,
        )
    
    def describe(
        self,
        repository: str,
        location: str,
    ):
        command = [
            "gcloud", "artifacts", "repositories", "describe", repository,
            f"--location={location}",
        ]
        self.run_sh(
            command=command,
        )
    
    def docker_auth(
        self,
        location,
    ):
        self.run_sh(
            command=["gcloud", "auth", "configure-docker", f"{location}-docker.pkg.dev"],
            inputs="yes\n",
        )
    
    def run_sh(
        self,
        command: list,
        inputs: str = None,
    ):
        result = subprocess.run(
            command,
            input=inputs,
            text=True,
            capture_output=True,
            shell=True,
        )
        event = result.stderr
        if "ALREADY_EXISTS" in event:
            logger.info("The repository already exists.")
        elif "NOT_FOUND" in event:
            self.rep_exists = False
            logger.error("The repository not found.")
        elif "registered correctly" in event:
            logger.info("gcloud credential helpers already registered correctly.")
        elif "Registry URL" in event:
            logger.info("The repository already exists.")
        else:
            logger.info(event)


class ToGCPImage(ArtifactRegistry):
    def __init__(
        self,
        project_id: str,
        location: str,
        repository: str,
        description: str,
    ):
        super().__init__()
        self.project_id = project_id
        self.location = location
        self.repository = repository
        self.description = description
        self.gcp_image = None
        self.docker_auth(location)
        self.describe(
            repository=repository,
            location=location,
        )
    
    def tag(
        self,
        source_image,
        gcp_image,
        tag=None,
    ):
        with docker_client() as client:
            try:
                local_image = client.images.get(source_image)
            except ImageNotFound:
                logger.info(f'Image not found: {source_image}.')
            
            if tag is None:
                self.gcp_image = f"{self.location}-docker.pkg.dev/{self.project_id}/{self.repository}/{gcp_image}"
            else:
                self.gcp_image = f"{self.location}-docker.pkg.dev/{self.project_id}/{self.repository}/{gcp_image}:{tag}"
            
            local_image.tag(self.gcp_image)
        return self
    
    def push(self):
        if self.gcp_image is None:
            logger.info("The local image is not tagged in artifact registry format.")
            return None
        if not self.rep_exists:
            self.create(
                self.repository,
                self.location,
                self.description,
            )
        
        with docker_client() as client:
            for event in client.images.push(self.gcp_image, stream=True, decode=True):
                status = event.get("status")
                if "error" in event:
                    logger.info(event["error"])
                elif "aux" in event:
                    logger.info(event["aux"])
                elif status in ["Preparing", "Waiting", "Pushing"]:
                    continue
                elif status == "Pushed":
                    logger.info(event)
                else:
                    logger.info(event)
