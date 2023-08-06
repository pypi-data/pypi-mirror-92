import os
from typing import Union

from google.cloud import secretmanager


def access_secret(secret_id: str, project_id: str = None, version_id: Union[str, int] = "latest"):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Get the default project id
    project_id = project_id if project_id is not None else os.getenv("GCP_PROJECT")

    if project_id is None:
        raise Exception("Cannot find project id. Please provide one or export it to GCP_PROJECT")

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    secret_resource_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret
    response = client.access_secret_version(name=secret_resource_name)

    # Return the secret
    payload = response.payload.data.decode("UTF-8")
    return payload
