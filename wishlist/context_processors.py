from .models import WishlistItem


def wishlist_items(request):
    """ Add wishlist items to request context. """

    if request.user.is_authenticated():
        return {
            'wishlist_items': WishlistItem.objects.filter(user=request.user)
        }

    # No user, no wishlist
    return {}
