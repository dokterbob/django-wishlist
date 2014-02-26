from .utils import SettingsBase


class WishlistSettings(SettingsBase):
    """ Settings specific to wishlists. """
    settings_prefix = 'WISHLIST'

    DEFAULT_REDIRECT_URL = 'wishlist'

wishlist_settings = WishlistSettings()
