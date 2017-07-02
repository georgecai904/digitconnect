from functional_tests.base import FunctionalTest
from unittest import skip

class PostPriceTest(FunctionalTest):

    @skip
    def test_purchaser_receive_suppliers_post(self):
        purchaser = self._create_purchaser()
        supplier1 = self._create_supplier(username="supplier1", name="1号供应商")
        supplier2 = self._create_supplier(username="supplier2", name="2号供应商")
        product = self._create_product(purchaser=purchaser)

        post_price1 = self._create_post_price(
            supplier=supplier1,
            product=product,
            price="100",
            amount="1000"
        )
        post_price2 = self._create_post_price(
            supplier=supplier2,
            product=product,
            price="99",
            amount="1000"
        )

        # 山姆今天又一次登陆了网站，他看到网页右上角显示了有最新报价

        # 山姆点击进去之后，看到一个产品列表页面，列表的最后一列是产品报价的人数

        # 山姆感到很兴趣，于是点击查看详情

        # 点击进去之后又是一个页面，上面详细描述了这个商品有哪几个供应商报价了

        # 山姆决定选择2号供应商，因为他的价格更加优惠，而且生产周期合适

        # 山姆点击2号供应商右边的确定采购

        # 页面跳转到了订单确认页面，左边是山姆作为采购商的信息，右边是2号供应商的所有信息，下面显示了商品信息

        # 山姆检查所有的信息，确认一切无误，页面下面的确认按钮

        # 页面提示山姆，订单已经生成，并已经将订单发送至2号供应商

        # 页面调回到了刚刚的报价列表，列表里刚刚已经生成订单的商品已经不在了

        # 山姆回到自己的产品页面，看到刚刚那个商品的状态已经更改为"已生成订单，等待供应商确认"

        # 山姆回到首页，发现刚刚那个商品已经从列表里面不存在了

        # 山姆很高兴的离开了

        # 2号供应商登陆了网刊

        # 2号供应商看到网页的右上角显示有最新订单

        # 2号供应商点击进入了一个订单列表，里面详细的记录了订单和订单状态，右边有一个查看详情

        # 点击查看详情后，页面进入到了订单页面，2号供应商检查一切信息都没有问题，并填写预计交割时间，并点击确认按钮

        # 点击确认按钮后，页面跳回到刚刚的订单列表，刚刚的订单状态为"已确认"

        # 2号供应商确认了一下预计订单时间填写正确，并离开了网站


