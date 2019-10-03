__author__ = "txy1226052@gmail.com"

from django.db.models.signals import post_delete
from django.dispatch import receiver

from user_operation.models import UserFav


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
