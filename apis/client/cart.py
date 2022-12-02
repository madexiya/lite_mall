from apis.base_api import BaseApi


class Cart(BaseApi):
    def add(self, goods_id, product_id):
        add_cart_url = "/wx/cart/add"
        cart_data = {"goodsId": goods_id, "number": 1, "productId": product_id}
        r = self.send("post", add_cart_url, json=cart_data, headers={"x-litemall-token": self.user_token})
        return r
