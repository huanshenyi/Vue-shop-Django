from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication


from .models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter


# Create your views here.
# ページング設定


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    # page_query_param = 'p'


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品リストページ,ページング，サーチ、フィルター，並び順
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication, ) goodsはログイン要らないのでなくていい
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    # https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    商品分類リストデータ
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearChsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
     """
     hot kwyword 取得
     """
     queryset = HotSearchWords.objects.all().order_by("-index")
     serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    swipperの画像を取得
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


    # 内容のフィルター追加 -->古い方式
    # def get_queryset(self):
    #     # querysetはsqlを作っただけで、実際取得までに行ってない,データの多さに気にすることはない
    #     queryset = Goods.objects.all()
    #     # フロントエンドからのパラメータを条件として,ここのgetはobject.get(key,default)
    #     price_min = self.request.query_params.get("price_min", 0)
    #     if price_min:
    #         queryset = queryset.filter(shop_price__gt=int(price_min))
    #     return queryset


    # def post(self, request, format=None):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    # from rest_framework import status
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
