from dataclasses import dataclass
from datetime import datetime

from gcloud_functions_utils.factories.triggers.pubsub import ContextEventType


@dataclass
class ContextMock:
    event_id: str = "600000000000000"
    timestamp: str = datetime.utcnow().isoformat("T") + "Z"
    event_type: str = str(ContextEventType.PubSubTopicPublish)
    resource: str = "projects/test-project/topics/test-topic"
