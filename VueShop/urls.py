"""VueShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
import xadmin
from VueShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


from goods.views import GoodsListViewSet, CategoryViewSet, HotSearChsViewset, BannerViewset, IndexCategoryViewset
# お気に入り
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
# user
from users.views import UserViewset
# ショッピングカート
from trade.views import ShoppingCartViewset
# オーダー
from trade.views import OrderViewset

router = DefaultRouter()
# goodsのurl設定
router.register(r'goods', GoodsListViewSet, base_name="goods")
# Categoryのurl設定
router.register('categorys', CategoryViewSet, base_name="categorys")
# ユーザー操作のurl設定(お気に入り)
router.register('userfavs', UserFavViewset, base_name="userfavs")
# 新規ユーザー用
router.register('user', UserViewset, base_name="users")
# メッセージ
router.register('message', LeavingMessageViewset, base_name="message")
# 送り先
router.register('address', AddressViewset, base_name="address")
# ショッピングカート
router.register("shopcarts", ShoppingCartViewset, base_name="shopcarts")
# オーダー
router.register("orders", OrderViewset, base_name="orders")
# 人気キーワード
router.register("hotsearchs", HotSearChsViewset, base_name="hotsearchs")
# swiper画像
router.register("banners", BannerViewset, base_name="banners")
# ホームページ商品シリーズデータ
router.register(r"indexGoods", IndexCategoryViewset, base_name="indexGoods")

# jwt認証
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # drfのドキュメント
    url(r'docs/', include_docs_urls(title="ドキュメント")),

    path('', include(router.urls)),
    # drf自分のtoken認証モード
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt認証
    url(r'^login/$', obtain_jwt_token),
    # 第三者サイトログイン
    url('', include('social_django.urls', namespace='social'))
]
