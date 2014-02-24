from .utils import SettingsBase


class WishlistSettings(SettingsBase):
    """ Settings specific to wishlists. """
    settings_prefix = 'WISHLIST'

    # DEFAULT_REQUEST_TIMEOUT = 5

wishlist_settings = WishlistSettings()
