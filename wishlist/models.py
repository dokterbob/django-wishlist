from django.db import models

from django.utils.translation import ugettext as _

from .settings import wishlist_settings

from .managers import UserManager

from .utils import get_user_model
User = get_user_model()


class WishlistItem(models.Model):
    """ Item in wishlist. """

    created = models.DateTimeField(_('created'), auto_now_add=True)

    user = models.ForeignKey(User)
    item = models.ForeignKey(wishlist_settings.ITEM_MODEL)

    objects = UserManager()

    class Meta:
        verbose_name = _('wishlist')
        verbose_name_plural = _('wishlists')
        ordering = ['-created']
        unique_together = ['user', 'item']

    def __unicode__(self):
        """ Wrap unicode of item. """

        assert self.item

        return unicode(self.item)

    def get_absolute_url(self):
        """ Return absolute URL for item. """

        return self.item.get_absolute_url()
