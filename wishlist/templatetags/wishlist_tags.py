from django import template

register = template.Library()

# from ..settings import wishlist_settings


def wishlist_form(context, item):
    """
    Render wishlist form for adding or removing a particular item.

    Assumes the user is available in the context and requires an instance of
    the wishlist model *not* WishlistItem.
    """

    # TODO: Replace by proper, meaningful, exceptions.
    assert 'user' in context
    # assert isinstance(item, wishlist_settings.ITEM_MODEL)
    assert hasattr(item, 'pk')
    assert hasattr(item, 'wishlistitem_set')

    return {
        'user': context['user'],
        'item': item
    }

# Register for adding
register.inclusion_tag(
    'wishlist/wishlistitem_add_form.html',
    takes_context=True, name='wishlist_add_form'
)(wishlist_form)

# Register for removing
register.inclusion_tag(
    'wishlist/wishlistitem_remove_form.html',
    takes_context=True, name='wishlist_remove_form'
)(wishlist_form)
