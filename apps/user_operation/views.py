from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from utils.permissions import IsOwnerOrReadOnly
from .serializers import UserFavSeriallzer


class UserFavViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    mixins.RetrieveModelMixin -> idを作る用
    お気に入り機能
    """
    # http://127.0.0.1:8000/userfavs/id/ method : DELETE 削除
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSeriallzer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "goods_id" # idをgoods_idに選択

    # 今ログインしてるユーザーだけのお気に入りを返す
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
    # ログインしてるかの判断
    # https://www.django-rest-framework.org/api-guide/permissions/#allowany  # IsAuthenticated

