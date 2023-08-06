import unittest
import json

from dingding_client.client import SendMessageToMq


class SendMessageToMqTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.exchange_name = "amq.direct"
        self.routing_key = "event"

    def testSend(self):
        try:
            client = SendMessageToMq(exchange_name=self.exchange_name, routing_key=self.routing_key)
            # client.send(json.dumps({'data': '测试'}))
            client.send("测试")
        except Exception as e:
            pass
