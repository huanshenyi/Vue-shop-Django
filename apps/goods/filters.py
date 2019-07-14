# url=https://django-filter.readthedocs.io/en/master/guide/rest_framework.html#quickstart
import django_filters
from .models import Goods


class GoodsFilter(django_filters.FilterSet):
    """
    商品フィルタークラス
    """
    price_min = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="shop_price", lookup_expr='let')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']