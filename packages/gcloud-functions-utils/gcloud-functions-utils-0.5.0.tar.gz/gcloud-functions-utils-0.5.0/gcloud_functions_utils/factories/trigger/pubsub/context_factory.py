from datetime import datetime
from typing import Union

from .context_event_type import ContextEventType
from .context_mock import ContextMock


class ContextFactory:
    @staticmethod
    def build(
        event_id: int = None, timestamp: datetime = None, event_type: Union[ContextEventType, str] = None, resource: str = None
    ):

        if event_id is None:
            event_id = 600000000000000

        formatted_event_id: str = str(event_id)

        if timestamp is None:
            timestamp = datetime.utcnow()

        formatted_timestamp: str = timestamp.isoformat("T") + "Z"

        if event_type is None:
            event_type = ContextEventType.PubSubTopicPublish

        if type(event_type) == ContextEventType:
            formatted_event_type = event_type.value
        elif type(event_type) == str and event_type in set(item.value for item in ContextEventType):
            formatted_event_type = str(event_type)
        else:
            raise Exception("Parameter event_type must be a value of ContextEventType (%s)" % str(event_type))

        if resource is None:
            resource = "projects/test-project/topics/test-topic"

        formatted_resource = str(resource)

        # Create the context object
        context_mock = ContextMock(
            event_id=formatted_event_id,
            timestamp=formatted_timestamp,
            event_type=formatted_event_type,
            resource=formatted_resource,
        )

        return context_mock
