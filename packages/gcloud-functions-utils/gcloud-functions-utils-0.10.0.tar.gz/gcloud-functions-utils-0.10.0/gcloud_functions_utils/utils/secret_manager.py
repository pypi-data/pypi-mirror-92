import os
from typing import Union

from google.cloud import secretmanager


class SecretManager:
    def __init__(self, project_id: str = None):
        # Get the default project id
        self.project_id = project_id if project_id is not None else os.getenv("GCP_PROJECT")

        if project_id is None:
            raise Exception("Cannot find project id. Please provide one or export it to GCP_PROJECT")

    def get(self, secret_id: str, version_id: Union[str, int] = "latest"):
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        secret_resource_name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret
        response = client.access_secret_version(name=secret_resource_name)

        # Return the secret
        payload = response.payload.data.decode("UTF-8")
        return payload
