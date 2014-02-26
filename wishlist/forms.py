from django.forms import ModelForm

from .models import WishlistItem


class WishlistItemForm(ModelForm):
    """ Form for WishlistItem. """

    class Meta:
        model = WishlistItem
        fields = ['item']
