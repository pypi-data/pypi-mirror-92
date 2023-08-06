# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import hashlib
import time
from lib.log import *
from conf.config import RETRY_COUNT, TIME_STEP


logger = logging.getLogger("dingding_notify")


def http_request(url, req_q, headers={'user-agent': 'shopex/spider'}):
    retry_count = RETRY_COUNT
    while 1:
        try:
            data = json.dumps(req_q.get(block=False))
        except Exception as e:
            time.sleep(2)
            continue
        while retry_count >= 0:
            try:
                req = urllib.request.Request(url, data.encode(), headers, method="POST")
                response = urllib.request.urlopen(req).read()
                response = json.loads(response)
                status = response.get("errmsg")
            except Exception as e:
                response = e
                status = 'fail'
                logger.error(e)

            if status != "ok":  # 尝试重发
                logger.error(response)
                retry_count -= 1
                continue
            else:
                time.sleep(TIME_STEP)
                break


def get_md5(string):
    try:
        m = hashlib.md5(string.encode(encoding='utf-8'))
        dest = m.hexdigest()
        return dest
    except Exception as e:
        logger.error(e)
        return False


def message_format(data):
    if not isinstance(data, dict):
        raise Exception("请传入正确的数据")
    event_time = time.strftime("%Y-%m-%d %H:%M:%S", data.get("timestamp", time.localtime()))
    event_main = data.get("main", "")
    event_service = data.get("service", "")
    event_message = data.get("message", "")
    return f"事件产生时间:{event_time}  事件产生主体:{event_main}  所属服务:{event_service}  事件内容:{event_message}"


if __name__ == '__main__':
    http_request(url="www.baidu.com")