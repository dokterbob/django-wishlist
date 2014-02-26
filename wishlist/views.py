from django.views.generic import ListView, CreateView, DeleteView
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.contrib import messages

from .settings import wishlist_settings
from .models import WishlistItem


class WishlistViewMixin(object):
    """ Common mixin for WishlistItem. """

    model = WishlistItem

    # TODO: Custom form
    fields = ['item']

    # TODO: Require login

    def get_queryset(self):
        """ Return only items for current user. """

        user = self.request.user
        assert user.is_authenticated(), \
            'View should not be accesible for unauthenticated users.'

        return super(WishlistViewMixin, self).get_queryset().filter(user=user)

    def get_success_url(self):
        """
        Allow specification of return URL using hidden form field or GET
        parameter, similar to auth views.

        1. Use 'next' POST parameter if available.
        2. Use 'next' GET parameter if available.
        3. Fall back to 'REDIRECT_URL' named URL, defaulting
           to 'wishlist' view.
        """

        redirect_to = self.request.POST.get(
            'next', self.request.GET.get('next', '')
        )

        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(wishlist_settings.REDIRECT_URL)

        return redirect_to


class WishlistView(WishlistViewMixin, ListView):
    """ View providing list if WishlistItem's for User. """

    pass


class WishlistAddView(WishlistViewMixin, CreateView):
    """ Add item to the wishlist. """

    def form_valid(self, form):
        """ Save and report to user. """

        # Set user
        form.instance.user = self.request.user

        # Call super
        result = super(WishlistAddView, self).form_valid(form)

        # Create message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Item {item} has been added to the wishlist.'.format(
                item=unicode(form.instance.item)
            )
        )

        # Return result of super
        return result


class WishlistRemoveView(WishlistViewMixin, DeleteView):
    """ Delete item from the wishlist. """

    def delete(self, request, *args, **kwargs):
        """ Delete and report to user. """

        # Call super
        result = super(WishlistRemoveView, self).delete(
            self, request, *args, **kwargs
        )

        # Create message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Item {item} has been removed from the wishlist.'.format(
                item=unicode(self.object)
            )
        )

        # Return result of super
        return result
