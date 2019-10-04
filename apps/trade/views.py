import time
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins

from .models import ShoppingCart, OrderInfo, OrderGoods
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    ショッピングカート
    list
      ショッピングカート詳細取得
    create:
      ショッピングカートに入れる
    delete
      記録を削除
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    # 検索用のidをpkから指定したキーに変更します
    lookup_field = "goods_id"  # https://blog.csdn.net/wu0che28/article/details/80981979

    def perform_create(self, serializer):
       shop_cart = serializer.save()
       goods = shop_cart.goods
       goods.goods_num -= shop_cart.goods_num
       goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.goods_num
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.goods_num
        saved_record = serializer.save()
        nums = saved_record.goods_num - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 現在ユーザーのだけの返す
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    オーダー管理
    list:
       個人的オーダーを取得
    delete:
       オーダーを削除
    create:
       新規オーダー
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # オーダー商品リストを表示
        if self.action == "retrieve":
            return OrderDetailSerializer
        # オーダーを表示
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.goods_num
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()
        return order