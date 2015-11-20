from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from django.views.generic import ListView, CreateView, DeleteView
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.http import is_safe_url
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _

from .settings import wishlist_settings
from .models import WishlistItem
from .forms import WishlistItemForm


class WishlistViewMixin(object):
    """ Common mixin for WishlistItem. """

    model = WishlistItem
    form_class = WishlistItemForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """ Require user login. """

        return super(WishlistViewMixin, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        """ Return only items for current user. """

        user = self.request.user
        assert user.is_authenticated(), \
            'View should not be accesible for unauthenticated users.'

        qs = super(WishlistViewMixin, self).get_queryset()

        return qs.for_user(user=user)

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
            redirect_to = reverse(wishlist_settings.REDIRECT_URL)

        return redirect_to


class WishlistView(WishlistViewMixin, ListView):
    """ View providing list if WishlistItem's for User. """

    pass


class WishlistClearView(WishlistViewMixin, ListView):
    """ Clear the wishlist. """

    template_name_suffix = '_confirm_clear'

    def post(self, *args, **kwargs):
        """ Delete and report to user. """

        # Delete all items
        self.get_queryset().delete()

        # Create message
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(u'The wishlist has been cleared.')
        )

        # Return result of super
        return HttpResponseRedirect(self.get_success_url())


class WishlistAddView(WishlistViewMixin, CreateView):
    """ Add item to the wishlist. """

    def form_valid(self, form):
        """ Save and report to user. """

        # Set user
        form.instance.user = self.request.user

        # Get created instance
        self.object = form.save(commit=False)

        # Validate uniqueness
        try:
            form.instance.validate_unique()

        except ValidationError:
            messages.add_message(
                self.request, messages.ERROR,
                _(u'Item {item} is already in the wishlist.').format(
                    item=unicode(form.instance.item)
                )
            )

            # Return redirect to success URL
            return HttpResponseRedirect(self.get_success_url())

        # Call super
        result = super(WishlistAddView, self).form_valid(form)

        # Create message
        messages.add_message(
            self.request, messages.SUCCESS,
            _(u'Item {item} has been added to the wishlist.').format(
                item=unicode(form.instance.item)
            )
        )

        # Return super
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
            _('Item {item} has been removed from the wishlist.').format(
                item=unicode(self.object)
            )
        )

        # Return result of super
        return result
