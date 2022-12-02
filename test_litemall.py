import json

import pytest
import requests

from log_utils import logger


class TestLiteMall:
    def setup_class(self):
        # 获取管理后台token
        url = "https://litemall.hogwarts.ceshiren.com/admin/auth/login"
        admin_data = {"username": "hogwarts", "password": "test12345", "code": ""}
        r = requests.post(url, json=admin_data)
        # print(r.json()["data"]["token"])
        self.admin_token = r.json()["data"]["token"]
        # 获取用户端token
        url = "https://litemall.hogwarts.ceshiren.com/wx/auth/login"
        user_data = {"username": "user123", "password": "user123"}
        r = requests.post(url, json=user_data)
        self.user_token = r.json()["data"]["token"]

    def teardown_method(self):
        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/delete"
        delete_data = {"id": self.goods_id}
        r = requests.post(url, json=delete_data, headers={"x-litemall-admin-token": self.admin_token})
        logger.info(f"删除商品接口响应为：{json.dumps(r.json(), ensure_ascii=False, indent=3)}")

    # 加入购物车整体流程
    @pytest.mark.parametrize("goods_name", ["小猫咪3", "小猫咪4"])
    def test_add_cart(self, goods_name):
        # goods_name = "小猫咪2"
        # 上架商品
        add_goods_url = "https://litemall.hogwarts.ceshiren.com/admin/goods/create"
        goods_data = {
            "goods": {"picUrl": "", "gallery": [], "isHot": False, "isNew": True, "isOnSale": True, "goodsSn": "120201",
                      "name": goods_name}, "specifications": [{"specification": "规格", "value": "标准", "picUrl": ""}],
            "products": [{"id": 0, "specifications": ["标准"], "price": 18, "number": 88, "url": ""}], "attributes": []}
        r = requests.post(add_goods_url, json=goods_data, headers={"x-litemall-admin-token": self.admin_token})
        # print(r.json())
        logger.info(f"上架商品接口响应为：{json.dumps(r.json(), ensure_ascii=False, indent=3)}")
        # 调用商品列表接口，获取商品id
        goods_list_url = "https://litemall.hogwarts.ceshiren.com/admin/goods/list"
        goods_param = {"name": goods_name,
                       "order": "desc",
                       "sort": "add_time"}
        r = requests.get(goods_list_url, params=goods_param, headers={"x-litemall-admin-token": self.admin_token})
        # print(r.json()["data"]["list"][0]["id"])
        logger.info(f"商品列表接口响应为：{json.dumps(r.json(), ensure_ascii=False, indent=3)}")
        self.goods_id = r.json()["data"]["list"][0]["id"]
        # 调用商品详情获取product_id
        goods_detail_url = "https://litemall.hogwarts.ceshiren.com/admin/goods/detail"
        detail_param = {"id": self.goods_id}
        r = requests.get(goods_detail_url, params=detail_param, headers={"x-litemall-admin-token": self.admin_token})
        # print(r.json()["data"]["products"][0]["id"])
        logger.info(f"商品详情接口响应为：{json.dumps(r.json(), ensure_ascii=False, indent=3)}")
        product_id = r.json()["data"]["products"][0]["id"]
        # 添加购物车
        add_cart_url = "https://litemall.hogwarts.ceshiren.com/wx/cart/add"
        cart_data = {"goodsId": self.goods_id, "number": 1, "productId": product_id}
        r = requests.post(add_cart_url, json=cart_data, headers={"x-litemall-token": self.user_token})
        res = r.json()
        logger.info(f"添加购物车接口响应结果：{json.dumps(res, ensure_ascii=False, indent=3)}")
        assert res["errmsg"] == "成功"
