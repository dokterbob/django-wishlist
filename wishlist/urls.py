from django.conf.urls import patterns, url

from .views import (
    WishlistView, WishlistAddView, WishlistClearView, WishlistRemoveView
)


urlpatterns = patterns('',
    url(r'^$',
        WishlistView.as_view(), name='wishlist'),
    url(r'^add/$',
        WishlistAddView.as_view(), name='wishlist_add'),
    url(r'^clear/$',
        WishlistClearView.as_view(), name='wishlist_clear'),
    url(r'^(?P<pk>\d+)/remove/$',
        WishlistRemoveView.as_view(), name='wishlist_remove'),
)
