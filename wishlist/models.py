from django.db import models

from .settings import wishlist_settings

from .utils import get_user_model
User = get_user_model()


class Wishlist(models.Model):
    """ Wishlist """
    user = models.ForeignKey(User)


class WishlistItem(models.Model):
    """ Item in wishlist. """
    wishlist = models.ForeignKey(Wishlist)
    item = models.ForeignKey(wishlist_settings.ITEM_MODEL)
