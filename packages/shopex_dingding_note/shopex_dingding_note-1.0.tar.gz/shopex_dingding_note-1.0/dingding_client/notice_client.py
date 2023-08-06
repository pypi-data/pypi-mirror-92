# -*- coding: utf-8 -*-
import time
import random
import threading
from gevent.queue import JoinableQueue


from lib.func_ext import get_md5, http_request
from lib.func_ext import message_format
from conf.config import MAXSIZE


class NoticeClient(object):
    init_flag = False
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # 双重检查锁定创建单例
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    return cls._instance
        else:
            return cls._instance

    def __init__(self, app_key, app_secret, api_url):
        if not self.init_flag:  # 防止重复执行init方法
            self.api_url = api_url
            self.app_key = app_key
            self.app_secret = app_secret
            self.req_q = JoinableQueue(MAXSIZE)
            self.init_flag = True
            t1 = threading.Thread(target=http_request, args=[self.api_url, self.req_q])
            t1.start()
        else:
            return

    def sys_params(self, body):
        """构造请求参数参数"""
        time.sleep(1)
        now = int(time.time())
        auth_key = '%d-%s-%s' % (now, self.app_secret, self.app_key)
        auth_key_md5 = get_md5(auth_key)
        auth_str = auth_key_md5[0:4] + str(random.randint(100, 999)) + auth_key_md5[4:24] + str(
            random.randint(10000, 99999)) + auth_key_md5[24:]
        _params = {
            "key": self.app_key,
            "auth_str": auth_str,
            "timestamp": now,
            "req_msg": body,
        }
        return _params

    def send(self, data, to_users):
        to_users = "|".join(to_users)
        data = message_format(data)
        body = {
            "to_user": to_users,
            "content": data
        }
        _params = self.sys_params(body)
        self.req_q.put(_params)

        return True