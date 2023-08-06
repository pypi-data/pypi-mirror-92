LOG_LEVEL = "INFO"

RETRY_COUNT = 3  # 发送消息到钉钉或mq失败时，重试次数

MAXSIZE = 1000  # 内存中存放发送请求的最大容纳量

TIME_STEP = 10  # 发送消息到钉钉的时间间隔，建议不要调太低，否则会有信息丢失问题