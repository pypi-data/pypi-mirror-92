import os
from typing import Union

from google.cloud import secretmanager


class SecretManager:
    def __init__(self, project_id: str = None, check_env: bool = False):
        self.check_env = check_env

        # Get the default project id
        self.project_id = project_id if project_id is not None else os.getenv("GCP_PROJECT")

        if self.project_id is None:
            raise Exception("Cannot find project id. Please provide one or export it to GCP_PROJECT")

    @property
    def client(self):
        # Only create the secretmanager on demand
        if self._client is None:
            # Create the Secret Manager client.
            self._client = secretmanager.SecretManagerServiceClient()

        return self._client

    def get(self, secret_id: str, version_id: Union[str, int] = "latest"):
        if self.check_env and secret_id in os.environ:
            return os.getenv(secret_id)

        # Build the resource name of the secret version.
        secret_resource_name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret
        response = self.client.access_secret_version(name=secret_resource_name)

        # Return the secret
        payload = response.payload.data.decode("UTF-8")
        return payload
