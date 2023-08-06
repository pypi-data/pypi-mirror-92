import json
import os
from typing import Dict, List, Union

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.futures import Future


class PubSubClient:
    def __init__(self, project_id: str = None):
        if project_id is not None:
            self.initial_project_id = project_id
        else:
            self.initial_project_id = None

        self.publisher = pubsub_v1.PublisherClient()

    @property
    def project_id(self):
        if self.initial_project_id is not None:
            return self.initial_project_id
        else:
            env_project_id = os.getenv("GCP_PROJECT")
            if env_project_id is not None:
                return env_project_id
            else:
                raise Exception("Cannot find project id. Please provide one or export it to GCP_PROJECT")

    def get_topic_path(self, topic_id: str, project_id: str = None) -> str:
        project_id = project_id if project_id is not None else self.project_id
        return self.publisher.topic_path(project_id, topic_id)

    def publish(
        self,
        topic_id: str,
        data: Union[str, int, Dict, List],
        attributes: Dict = None,
        ordering_key: str = None,
        project_id: str = None,
    ):
        topic_path = self.get_topic_path(topic_id, project_id)

        cleaned_data = PubSubClient._clean_data(data)
        encoded_data = cleaned_data.encode("utf-8")

        kwargs = {}
        if type(attributes) == dict and attributes is not None:
            for attr_key, attr_value in attributes.items():
                kwargs[attr_key] = attr_value
        if ordering_key is not None and len(ordering_key) > 0:
            kwargs["ordering_key"] = ordering_key

        future = self.publisher.publish(topic=topic_path, data=encoded_data, **kwargs)

        return future

    @staticmethod
    def _clean_data(data):
        data_type = type(data)
        if data_type == str:
            return data
        elif data_type == int:
            return str(data)
        elif data_type == dict or data_type == list:
            return json.dumps(data)
        else:
            return str(data)
