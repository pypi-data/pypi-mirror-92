import base64
from datetime import datetime
from typing import Dict


class EventFactory:
    @staticmethod
    def build(
        data: str = None,
        attributes: Dict = None,
        message_id: int = None,
        publish_time: datetime = None,
        ordering_key: str = None,
    ) -> Dict:
        # Set default values of provided parameters

        if data is None:
            data = ""

        if message_id is None:
            message_id = 600000000000000

        formatted_message_id = str(message_id)

        if publish_time is None:
            publish_time = datetime.utcnow()

        formatted_publish_time = publish_time.isoformat("T") + "Z"

        # Create the event object
        event = {
            "data": base64.b64encode(data.encode("utf-8")),
            "messageId": formatted_message_id,
            "publishTime": formatted_publish_time,
        }

        # Fill with optional values

        if attributes is not None:
            event["attributes"] = attributes

        if ordering_key is not None:
            event["orderingKey"] = str(ordering_key)

        return event
