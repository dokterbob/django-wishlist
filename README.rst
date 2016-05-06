###############
django-wishlist
###############

.. image:: https://img.shields.io/pypi/v/django-wishlist.svg
    :target: https://pypi.python.org/pypi/django-wishlist

.. image:: https://img.shields.io/travis/dokterbob/django-wishlist/master.svg
    :target: http://travis-ci.org/dokterbob/django-wishlist

.. image:: https://coveralls.io/repos/dokterbob/django-wishlist/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/dokterbob/django-wishlist?branch=master

.. image:: https://landscape.io/github/dokterbob/django-wishlist/master/landscape.svg?style=flat
   :target: https://landscape.io/github/dokterbob/django-wishlist/master
   :alt: Code Health

Generic user wishlists for use with any Django model.
-----------------------------------------------------

What is it?
===========
Generic user wishlists for shops and the likes.

Status
======
Alpha. Don't use it, unless you're willing to fix issues. Will be released
on PyPI as soon as tested in limited production.

Compatibility
=============
Tested to work with Django 1.8 and 1.9 and Python 2.7.

Requirements
============
Please refer to `requirements.txt <http://github.com/dokterbob/django-wishlist/blob/master/requirements.txt>`_
for an updated list of required packages.

Installation
============

The package is available

To install:

1. Install the django-wishlist app::

    pip install django-wishlist

2. In your Django settings:

   - Add `'wishlist'` to `INSTALLED_APPS`.

   - Configure `WISHLIST_ITEM_MODEL` to the model used for wishlist items.

   - Optionally: add `wishlist.context_processors.wishlist_items` to your
     `TEMPLATE_CONTEXT_PROCESSORS`.

   For example::

        INSTALLED_APPS = [
            ...
            'wishlist'
            ...
        ]

        TEMPLATE_CONTEXT_PROCESSORS = [
            ...
            'wishlist.context_processors.wishlist_items',
            ...
        ]

        WISHLIST_ITEM_MODEL = 'my_webshop.Product'

3. In `urls.py` add::

       (r'^/wishlist/', include('wishlist.urls')),

4. Update the database::

       ./manage.py migrate

   Note Migrations do not work as the model is dynamically configured.

Usage
===========

Create a button to add an item to the wishlist simply from within your template.

At the top of the page add::

    {% load wishlist_tags %}

And where you want the button add::

    {% wishlist_add_form product %}

Where product is the product you want to add to the wishlist.

Tests
==========
Tests for pull req's and the master branch are automatically run through
`Travis CI <http://travis-ci.org/dokterbob/django-wishlist>`_.

License
=======
This application is released
under the GNU Affero General Public License version 3.
