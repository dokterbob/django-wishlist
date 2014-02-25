from django.views.generic import ListView, CreateView, DeleteView

from .models import WishlistItem


class WishlistViewMixin(object):
    """ Common mixin for WishlistItem. """

    model = WishlistItem

    def get_queryset(self):
        """ Return only items for current user. """

        user = self.request.user
        assert user.is_authenticated(), \
            'View should not be accesible for unauthenticated users.'

        return super(WishlistView, self).get_queryset().filter(user=user)


class WishlistView(WishlistViewMixin, ListView):
    """ View providing list if WishlistItem's for User. """

    pass


class WishlistAddView(WishlistViewMixin, CreateView):
    """ Add item to the wishlist. """

    pass


class WishlistRemoveView(WishlistViewMixin, DeleteView):
    """ Delete item from the wishlist. """

    pass
