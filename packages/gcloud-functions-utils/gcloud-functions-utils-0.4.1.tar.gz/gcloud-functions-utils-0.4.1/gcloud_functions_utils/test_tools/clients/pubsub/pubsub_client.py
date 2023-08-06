import base64
import inspect
import json
import os
import subprocess
from typing import Callable, Dict

import requests
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class PubSubPublisher:
    def __init__(self, url: str, session: Session, process: subprocess.Popen):
        self.url = url
        self.session = session
        self.process = process

    def publish(self, data, attributes: Dict = None):
        encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        pubsub_message = {"data": {"data": encoded_data}}

        if attributes is not None:
            pubsub_message["data"]["attributes"] = attributes

        return self.session.post(self.url, json=pubsub_message)

    def get_raw_output(self):
        self.process.kill()
        self.process.wait()
        return self.process.communicate()

    def get_output(self):
        output, _ = self.get_raw_output()
        return output.decode("utf-8")

    def get_json(self):
        output = self.get_output()
        return json.loads(output.replace("'", '"'))


class PubSubClient:
    def __init__(self, func: Callable, port: int = 8888):
        self.func = func
        self.port = port
        self.url = f"http://localhost:{self.port}/"
        self.retry_adapter = HTTPAdapter(max_retries=Retry(total=6, backoff_factor=1))

        self.target = self.func.__name__
        self.source = inspect.getfile(self.func)

    def __enter__(self):
        self.session = requests.Session()
        self.session.mount(self.url, self.retry_adapter)

        self.process: subprocess.Popen = subprocess.Popen(
            [
                "functions-framework",
                "--target",
                self.target,
                "--source",
                self.source,
                "--signature-type",
                "event",
                "--port",
                str(self.port),
            ],
            cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE,
        )

        return PubSubPublisher(self.url, self.session, self.process)

    def __exit__(self, exception_type, exception_value, traceback):
        if self.process.poll() is None:
            self.process.kill()
            self.process.wait()
