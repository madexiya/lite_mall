import requests

from apis.base_api import BaseApi


class Goods(BaseApi):
    def create(self, goods_data):
        add_goods_url = "/admin/goods/create"
        # r = requests.post(add_goods_url, json=goods_data,
        #                   headers={"x-litemall-admin-token": self.admin_token})
        r = self.send("post", add_goods_url, json=goods_data,
                      headers={"x-litemall-admin-token": self.admin_token})
        return r

    def list(self, goods_name, order="desc", sort="add_time"):
        goods_list_url = "/admin/goods/list"
        goods_param = {"name": goods_name,
                       "order": order,
                       "sort": sort}
        r = self.send("get", goods_list_url, params=goods_param,
                      headers={"x-litemall-admin-token": self.admin_token})
        return r

    def detail(self, goods_id):
        goods_detail_url = "/admin/goods/detail"
        detail_param = {"id": goods_id}
        r = self.send("get", goods_detail_url, params=detail_param,
                      headers={"x-litemall-admin-token": self.admin_token})
        return r

    def delete(self, goods_id):
        url = "/admin/goods/delete"
        delete_data = {"id": goods_id}
        r = self.send("post", url, json=delete_data, headers={"x-litemall-admin-token": self.admin_token})
        return r
