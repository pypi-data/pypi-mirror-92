import base64
import binascii
from datetime import datetime
from typing import Dict, Union, Any


class EventParser:

    data: str
    attributes: Dict[str, str]
    message_id: int
    publish_time: datetime
    orderingKey: Union[str, None]

    def __init__(self, event: Union[Dict, Any]):
        if "data" in event:
            try:
                self.data: str = base64.b64decode(event["data"]).decode("utf-8")
            except binascii.Error:
                pass
        else:
            self.data = ""

        if "attributes" in event:
            self.attributes: Dict[str, str] = event["attributes"]
        else:
            self.attributes = {}

        if "messageId" in event:
            self.message_id: int = int(event["messageId"])
        else:
            self.message_id = -1

        if "publishTime" in event:
            self.publish_time: datetime = datetime.strptime(event["publishTime"], "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            self.publish_time = datetime.fromtimestamp(0)

        if "orderingKey" in event:
            self.ordering_key: str = event["orderingKey"]
        else:
            self.orderingKey = None
