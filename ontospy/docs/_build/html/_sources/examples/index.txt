.. djfacet documentation master file, created by
   sphinx-quickstart on Tue May 31 11:14:57 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DJFacet's documentation!
===================================

Django Faceted Browser is a `Django <https://www.djangoproject.com/>`_ application that allows you to navigate your data using an approach based on 'dynamic taxonomies', also known as 'facets'.

The application relies heavily on `Django's database API <https://docs.djangoproject.com/en/1.3/topics/db/queries/>`_, so it requires some working knowledge of Django and especially of the `model layer <https://docs.djangoproject.com/en/1.3/topics/db/models/>`_. In short, if you have completed the online Django `tutorial <https://docs.djangoproject.com/en/1.3/intro/tutorial01/>`_ or have already developed web apps using Django, you're likely to get the most out of DJFacet too.


At a glance
------------

DJFacet is an easy-to-use faceted search system built on top of the Django python framework. Its main features are:

- Rapid installation and integration with existing Django projects
- It's back-end agnostic (as it rests on Django's Database API)
- Has a minimal and customisable look and feel, based on templates overriding
- It follows a REST architecture: urls of a search are stable and bookmark-able 
- It supports pivoting (the type of objects being searched for can be changed dynamically) 
- It provides a dedicated caching system (useful for apps with many facets/zoom points)

If you have no time to go through the documentation but you'd like to see what DJFacet is about, just `try out the demo application <http://www.michelepasin.org/demos/djfacet/>`_  (the application lets you browse a sample database on the distribution of religions in world's countries).


Contents
-----------
.. toctree::
   :maxdepth: 2
   
   intro
   installation
   settings
   configuration
   templates
   caching
   commands
   demo
   license


Indices and tables
-------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

