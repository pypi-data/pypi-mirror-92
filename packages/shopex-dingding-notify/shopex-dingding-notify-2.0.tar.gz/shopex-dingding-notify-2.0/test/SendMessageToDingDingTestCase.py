import time
import unittest

from dingding_client.client import SendMessageToDingDing


class SendMessageToDingDingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app_key = "xxx"
        self.app_secret = "xxx"
        self.api_url = "xxx"

    def testSend(self):
        client = SendMessageToDingDing(app_key=self.app_key, app_secret=self.app_secret, api_url=self.api_url)
        try:
            # 第一个参数是一个列表，表示要发送给谁
            # 第二个参数也是一个列表， 表示mq消息队列
            client.start(["s4261"], ["dingding"])
        except Exception as e:
            pass

        while 1:
            time.sleep(10)