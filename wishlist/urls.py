from django.conf.urls import patterns, url

from .views import WishlistView, WishlistAddView, WishlistRemoveView


urlpatterns = patterns('',
    url(r'^$', WishlistView.as_view(), name='wishlist'),
    url(r'^add/$', WishlistAddView.as_view(), name='wishlist_add'),
    url(r'^(?P<pk>\d+)/$', WishlistRemoveView.as_view(), name='wishlist_remove'),
)
