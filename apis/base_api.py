import json
import requests

from utils.log_utils import logger


class BaseApi:
    def __init__(self, base_url):
        self.base_url = base_url
        # 获取管理后台token
        admin_url = "/admin/auth/login"
        admin_data = {"username": "hogwarts", "password": "test12345", "code": ""}
        admin_res = self.send("post", admin_url, json=admin_data)
        self.admin_token = admin_res["data"]["token"]
        # 获取用户端token
        user_url = "/wx/auth/login"
        user_data = {"username": "user123", "password": "user123"}
        user_res = self.send("post", user_url, json=user_data)
        self.user_token = user_res["data"]["token"]

    def send(self, method, url, **kwargs):
        r = requests.request(method, self.base_url + url, **kwargs)
        logger.debug(f"{url}接口的响应为：{json.dumps(r.json(), ensure_ascii=False, indent=3)}")
        return r.json()
