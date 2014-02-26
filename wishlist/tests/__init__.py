from django.test.utils import override_settings

from django.core.urlresolvers import reverse

from django_dynamic_fixture import N, G

from django_webtest import WebTest

from ..models import WishlistItem
from ..utils import get_user_model
User = get_user_model()

from .models import TestItemModel


@override_settings(WISHLIST_ITEM_MODEL='tests.TestItemModel')
class WishlistTests(WebTest):
    """ Unit and functional tests for wishlists. """

    def test_save(self):
        """ Test saving a WishlistItem. """

        # Create
        item = N(WishlistItem)

        # Validate
        item.clean()

        # Save
        item.save()

    def test_unicode(self):
        item = G(WishlistItem)

        self.assertEquals(unicode(item), unicode(item.item))

    def test_absolute_url(self):
        item = G(WishlistItem)

        self.assertEquals(
            item.get_absolute_url(),
            item.item.get_absolute_url()
        )

    def test_login_required(self):
        """ Assure login is required. """

        view = reverse('wishlist_add')

        result = self.app.get(view)

        self.assertEquals(result.status_int, 302)
        self.assertIn('login', result.url)

    def test_add(self):
        """ Test adding an item. """

        # Get URL for add view
        add_view = reverse('wishlist_add')

        # Create an item to add
        wished_item = G(TestItemModel, slug='test')

        # Create a user and login
        user = G(User)

        # Request add view
        add_page = self.app.get(add_view, user=user)

        # Fill in form and post
        add_form = add_page.form
        add_form['item'] = wished_item.pk
        add_result = add_form.submit()

        # Assert WishlistItem has been created
        self.assertEquals(WishlistItem.objects.count(), 1)

        item = WishlistItem.objects.get()
        self.assertEquals(item.user, user)
        self.assertEquals(item.item_id, wished_item.pk)

        # Test redirect after adding
        result = add_result.follow()

        # Test messages after adding
        self.assertContains(result, unicode(item))
        self.assertContains(result, u'added to the wishlist')

    def test_remove_confirm(self):
        """ Test removal confirm form. """

        # Create wishlist item
        item = G(WishlistItem)

        # Get URL for remove view
        remove_view = reverse('wishlist_remove', kwargs=dict(pk=item.pk))

        # Request view
        page = self.app.get(remove_view, user=item.user)
        self.assertContains(page, 'Confirm')

        # Post form
        page.form.submit()

        # Assert WishlistItem has been removed
        self.assertEquals(WishlistItem.objects.count(), 0)

    def test_remove(self):
        """ Test removing an item. """

        # Create wishlist item
        item = G(WishlistItem)

        # Get URL for list view
        list_view = reverse('wishlist')

        # Request view
        list_page = self.app.get(list_view, user=item.user)

        # Find and post remove form
        remove_form = list_page.form
        remove_result = remove_form.submit()

        # Assert WishlistItem has been removed
        self.assertEquals(WishlistItem.objects.count(), 0)

        # Perform redirect after adding
        result = remove_result.follow()

        # Test messages after adding
        self.assertContains(result, unicode(item))
        self.assertContains(result, u'removed from the wishlist')

    def test_permission(self):
        """ List for one user should be empty for another. """

        # Create wishlist item
        item = G(WishlistItem)

        # Get URL for list view
        list_view = reverse('wishlist')

        # Request view
        list_page = self.app.get(list_view, user=item.user)

        # Item for creating user
        self.assertContains(list_page, unicode(item))

        # Request view with another user
        list_page = self.app.get(list_view, user=G(User))

        # No item for other user
        self.assertNotContains(list_page, unicode(item))

    def test_clear(self):
        """ Test clearing the wishlist. """

        # Begin at list view with single item
        # Create wishlist item
        item = G(WishlistItem)

        # Get URL for list view
        list_view = reverse('wishlist')

        # Request view
        list_page = self.app.get(list_view, user=item.user)

        # Click clear button
        clear_page = list_page.click('Clear wishlist')
        self.assertContains(clear_page, 'Confirm')

        # Post form
        clear_page.form.submit()

        # Assert WishlistItem has been removed
        self.assertEquals(WishlistItem.objects.count(), 0)
