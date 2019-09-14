from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import ShoppingCart
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCartDetailSerializer


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

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    # 現在ユーザーのだけの返す
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
