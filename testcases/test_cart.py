import pytest

from apis.admin.goods import Goods
from apis.client.cart import Cart


class TestCart:
    def setup_class(self):
        self.goods = Goods("https://litemall.hogwarts.ceshiren.com")
        self.cart = Cart("https://litemall.hogwarts.ceshiren.com")

    @pytest.mark.parametrize("goods_name", ["小猫咪3", "小猫咪4"])
    def test_add_cart(self, goods_name):
        goods_data = {
            "goods": {"picUrl": "", "gallery": [], "isHot": False, "isNew": True, "isOnSale": True, "goodsSn": "120201",
                      "name": goods_name}, "specifications": [{"specification": "规格", "value": "标准", "picUrl": ""}],
            "products": [{"id": 0, "specifications": ["标准"], "price": 18, "number": 88, "url": ""}], "attributes": []}
        self.goods.create(goods_data)
        goods_id = self.goods.list(goods_name)["data"]["list"][0]["id"]
        product_id = self.goods.detail(goods_id)["data"]["products"][0]["id"]
        add_res = self.cart.add(goods_id, product_id)
        assert add_res["errmsg"] == "成功"
        delete_res = self.goods.delete(goods_id)
        assert delete_res["errmsg"] == "成功"
