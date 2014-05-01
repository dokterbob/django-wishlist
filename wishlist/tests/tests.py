from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import RequestFactory

from django.core.urlresolvers import reverse
from django.template import Template, Context

from django.contrib.auth.models import AnonymousUser

from django_dynamic_fixture import N, G

from django_webtest import WebTest
from webtest.response import TestResponse

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

    def test_add_form(self):
        """ Test wishlist_add_form template tag. """

        # Create one wished item for testing
        wished_item = G(TestItemModel)

        # Get URL for add view
        add_view = reverse('wishlist_add')

        # Create user for testing
        user = G(User)

        # Setup and render template
        template = Template(
            '{% load wishlist_tags %}{% wishlist_add_form item %}'
        )
        context = Context(dict(item=wished_item, user=user))
        rendered = template.render(context)

        # Test output
        self.assertHTMLEqual(
            '<form action="{0}" method="post">'
            '<input type="hidden" name="item" value="{1}">'
            '<input type="submit" value="Add">'
            '</form>'.format(add_view, wished_item.pk),
            rendered
        )

    def test_remove_form(self):
        """ Test wishlist_remove_form template tag. """

        # Create one item for testing
        wishlist_item = G(WishlistItem)

        # Remove url
        remove_view = reverse(
            'wishlist_remove', kwargs=dict(pk=wishlist_item.pk)
        )

        # Setup and render template
        template = Template(
            '{% load wishlist_tags %}{% wishlist_remove_form item %}'
        )
        context = Context(
            dict(item=wishlist_item.item, user=wishlist_item.user)
        )
        rendered = template.render(context)

        # Test output
        self.assertHTMLEqual(
            '<form action="{0}" method="post">'
            '<input type="submit" value="Remove">'
            '</form>'.format(
                remove_view
            ), rendered
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
        list_view = reverse('wishlist')

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

        # Assert redirect location
        self.assertTrue(add_result.location.endswith(list_view))

        # Test redirect after adding
        result = add_result.follow()

        # Test messages after adding
        self.assertContains(result, unicode(item))
        self.assertContains(result, u'added to the wishlist')

    def test_add_twice(self):
        """
        Test adding an item twice.

        Should add a warning message and not generate an exception.
        """

        # Get URL for add view
        add_view = reverse('wishlist_add')
        list_view = reverse('wishlist')

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

        # Test redirect after adding
        result = add_result.follow()
        self.assertContains(result, u'added to the wishlist')

        # Post again
        add_result = add_form.submit()

        # Assert WishlistItem still in wishlist
        self.assertEquals(WishlistItem.objects.count(), 1)

        # Assert redirect location
        self.assertTrue(add_result.location.endswith(list_view))

        # Test redirect after adding
        result = add_result.follow()

        # Test redirect after adding
        self.assertContains(result, u'already in the wishlist')

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
