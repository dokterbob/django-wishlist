from django.test import TestCase
from django.test.utils import override_settings


@override_settings(WISHLIST_ITEM_MODEL='tests.TestItemModel')
class WishlistTests(TestCase):
    def test_meuk(self):
        """ Test the meuk. """

        self.assertTrue(True)
