from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import RequestFactory

from django.contrib.auth.models import AnonymousUser

from django.core.urlresolvers import reverse

from django_dynamic_fixture import N, G

from django_webtest import WebTest

from ..models import WishlistItem
from ..utils import get_user_model
User = get_user_model()

from ..context_processors import wishlist_items

from .models import TestItemModel


@override_settings(WISHLIST_ITEM_MODEL='tests.TestItemModel')
class WishlistUnitTests(TestCase):
    """ Unit tests for wishlists. """

    def test_save(self):
        """ Test saving a WishlistItem. """

        # Create
        item = N(WishlistItem)

        # Validate
        item.clean()

        # Save
        item.save()

    def test_unicode(self):
        """ Test __unicode__ """
        item = G(WishlistItem)

        self.assertEquals(unicode(item), unicode(item.item))

    def test_absolute_url(self):
        """ Test get_absolute_url() """
        item = G(WishlistItem)

        self.assertEquals(
            item.get_absolute_url(),
            item.item.get_absolute_url()
        )

    def test_manager(self):
        """ Test custom user manager """

        # Create two users and wishlist items
        user1 = G(User)
        user2 = G(User)

        item1 = G(WishlistItem, user=user1)
        item2 = G(WishlistItem, user=user2)

        # Only this item should be available
        self.assertEquals(
            WishlistItem.objects.for_user(user=user1).count(),
            1
        )

        self.assertEquals(
            WishlistItem.objects.for_user(user=user1)[0],
            item1
        )

        self.assertEquals(
            WishlistItem.objects.for_user(user=user2).count(),
            1
        )

        self.assertEquals(
            WishlistItem.objects.for_user(user=user2)[0],
            item2
        )

    def test_context_processor(self):
        """ Test wishlist_items context processor. """

        # Create one item for testing
        item = G(WishlistItem)

        # Request factory and request
        factory = RequestFactory()
        request = factory.get('/')

        # Anonymous user
        request.user = AnonymousUser()

        # No context for anonymous users
        result = wishlist_items(request)
        self.assertEquals(result, {})

        # User set, should return items for user
        request.user = item.user
        result = wishlist_items(request)

        self.assertEquals(len(result['wishlist_items']), 1)

        self.assertEquals(
            result['wishlist_items'][0],
            WishlistItem.objects.for_user(user=item.user)[0]
        )


@override_settings(WISHLIST_ITEM_MODEL='tests.TestItemModel')
class WishlistFunctionalTests(WebTest):
    """ Functional/integration tests for views. """

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

    def test_list(self):
        """ Test list view. """

        # Create wishlist item
        item = G(WishlistItem)

        # Get URL for list view
        list_view = reverse('wishlist')

        # Request view
        list_page = self.app.get(list_view, user=item.user)

        self.assertContains(list_page, unicode(item))
        self.assertContains(list_page, item.get_absolute_url())
        self.assertContains(list_page, '1 item in wishlist')

        # Add another item for same user
        item2 = G(WishlistItem, user=item.user)

        # Request view
        list_page = self.app.get(list_view, user=item.user)

        self.assertContains(list_page, unicode(item))
        self.assertContains(list_page, item.get_absolute_url())
        self.assertContains(list_page, unicode(item2))
        self.assertContains(list_page, item2.get_absolute_url())
        self.assertContains(list_page, '2 items in wishlist')

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


