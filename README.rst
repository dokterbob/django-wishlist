=================
django-wishlist
=================

.. image:: https://secure.travis-ci.org/dokterbob/django-wishlist.png?branch=master
    :target: http://travis-ci.org/dokterbob/django-wishlist

.. .. image:: https://coveralls.io/repos/dokterbob/django-wishlist/badge.png
..     :target: https://coveralls.io/r/dokterbob/django-wishlist

.. image:: https://landscape.io/github/dokterbob/django-wishlist/master/landscape.png
   :target: https://landscape.io/github/dokterbob/django-wishlist/master
   :alt: Code Health

.. .. image:: https://badge.fury.io/py/django-wishlist.png
..    :target: http://badge.fury.io/py/django-wishlist

.. .. image:: https://pypip.in/d/django-wishlist/badge.png
..    :target: https://crate.io/packages/django-wishlist?version=latest

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
Tested to work with Django 1.4, 1.5 and 1.6 and Python 2.6 as well as 2.7.

Requirements
============
Please refer to `requirements.txt <http://github.com/dokterbob/django-wishlist/blob/master/requirements.txt>`_
for an updated list of required packages.

Installation
============

The package is available

To install:

1. Install the django-wishlist app::

    pip install -e git+https://github.com/dokterbob/django-wishlist.git#egg=django-wishlist

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

       ./manage.py syncdb

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
