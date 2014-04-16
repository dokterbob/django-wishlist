from django import template

from copy import copy

register = template.Library()


def wishlist_form(context, item):
    """
    Render wishlist form for adding or removing a particular item.

    Assumes the user is available in the context and requires an instance of
    the wishlist model *not* WishlistItem.
    """

    # TODO: Replace by proper, meaningful, exceptions.
    assert 'user' in context
    assert hasattr(item, 'pk')
    assert hasattr(item, 'wishlistitem_set')

    # Copy local context dict, including
    context = copy(context)

    # Add item
    context['item'] = item

    # Return context for use in inclusion tag
    return context

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
