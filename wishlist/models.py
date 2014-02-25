from django.db import models

from django.utils.translation import ugettext as _

from .settings import wishlist_settings

from .utils import get_user_model
User = get_user_model()


class WishlistItem(models.Model):
    """ Item in wishlist. """
    item = models.ForeignKey(wishlist_settings.ITEM_MODEL)

    class Meta:
        verbose_name = _('wishlist')
        verbose_name_plural = _('wishlists')
