from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from utils.permissions import IsOwnerOrReadOnly
from .serializers import UserFavSeriallzer, UserFavDetailSerializer, LeavingMessageSerializer, AddressSerializer


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    mixins.RetrieveModelMixin -> idを作る用
    お気に入り機能
    list -> ユーザーお気に入りリスト取得
    retrieve -> とある商品お気に入りかどうか
    create -> 商品をお気に入り登録
    """
    # http://127.0.0.1:8000/userfavs/id/ method : DELETE 削除
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id" # idをgoods_idに選択

    # 今ログインしてるユーザーだけのお気に入りを返す
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
    # ログインしてるかの判断
    # https://www.django-rest-framework.org/api-guide/permissions/#allowany  # IsAuthenticated

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSeriallzer
        return UserFavSeriallzer


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
      """
      list:
        ユーザーメッセージ取得
      create:
        メッセージ挿入
      delete:
        メッセージ削減
      """
      permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
      serializer_class = LeavingMessageSerializer
      authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
      def get_queryset(self):
          return UserLeavingMessage.objects.filter(user=self.request.user)


# viewsets.ModelViewSetすべてある
class AddressViewset(viewsets.ModelViewSet):
    """
    荷物受け取り住所管理
    list:
      住所取得
    create:
      新規 住所
    update:
      住所更新
    delete
      住所削除
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)



