from django.contrib import admin


from .models import WishlistItem


class WishlistItemAdmin(admin.ModelAdmin):
    """ Admin for WishlistItem. """

    pass

admin.site.register(WishlistItem, WishlistItemAdmin)
