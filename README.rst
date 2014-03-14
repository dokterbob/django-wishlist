=================
django-wishlist
=================

.. image:: https://secure.travis-ci.org/dokterbob/django-wishlist.png?branch=master
    :target: http://travis-ci.org/dokterbob/django-wishlist

.. image:: https://coveralls.io/repos/dokterbob/django-wishlist/badge.png
    :target: https://coveralls.io/r/dokterbob/django-wishlist

.. image:: https://landscape.io/github/dokterbob/django-wishlist/master/landscape.png
   :target: https://landscape.io/github/dokterbob/django-wishlist/master
   :alt: Code Health

.. image:: https://badge.fury.io/py/django-wishlist.png
    :target: http://badge.fury.io/py/django-wishlist

.. image:: https://pypip.in/d/django-wishlist/badge.png
    :target: https://crate.io/packages/django-wishlist?version=latest

Generic user wishlists for use with any Django model.
-----------------------------------------------------

What is it?
===========
TO BE DONE

Status
======
Early alpha. Don't use it, unless you're willing to fix issues.

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

1. In requirements.txt add::

   -e git+https://github.com/dokterbob/django-wishlist.git#egg=django-wishlist

2. In settings_default.py:

   - add 'wishlist' to INSTALLED_APPS. 

   - add WISHLIST_ITEM_MODEL = PRODUCT_MODEL
  
     PRODUCT_MODEL refers to the model of the product
     you want to be able to present in a wishlist.

   For example::
           
        INSTALLED_APPS = [
            'localeurl',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
                
            'wishlist'
        ]
            
        """ django-wishlist """
        WISHLIST_ITEM_MODEL = SHOPKIT_PRODUCT_MODEL

3. In urls.py add::

       (r'^/wishlist/', include('wishlist.urls')),

4. At the command line execute::

       pip install -r requirements.txt
       ./manage.py syncdb

Tests
==========
Tests for pull req's and the master branch are automatically run through
`Travis CI <http://travis-ci.org/dokterbob/django-wishlist>`_.

License
=======
This application is released
under the GNU Affero General Public License version 3.
