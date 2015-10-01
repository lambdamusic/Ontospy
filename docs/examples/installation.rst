Installation
************************
In this section we'll show how to install DJFacet.


Dependencies
=============

- Django 1.3 or above (`download <https://www.djangoproject.com/download/>`_). Older versions of Django haven't been tested, although they may work.
- Django picklefield (`download <http://pypi.python.org/pypi/django-picklefield>`_).
- **Optional**: Django MPTT (`download <http://code.google.com/p/django-mptt/>`_).

These libraries are needed for DJFacet to work: install them system-wide or elsewhere, as long as they can be located via your `PYTHONPATH <http://docs.python.org/using/cmdline.html#envvar-PYTHONPATH>`_ setting.

.. warning::

   Support for hierarchical facets via django-MPTT is still being tested and will be released in future versions  of DJFacet.


Step by step installation
=============================

	
Step 1: Download and unpack the application
++++++++++++++++++++++++++++++++++++++++++++

Download the latest version of DJFacet from google code: http://code.google.com/p/djfacet/downloads/list

Expand the package just downloaded and put it in a suitable location. This can be the same folder as the django project you're working on, or any other location, as long as it is in your PYTHONPATH::

	$ tar xfz djfacet-VERSION.tar.gz
	$ cp -r djfacet /path/to/my/project/



Step 2: Add the application to your project
++++++++++++++++++++++++++++++++++++++++++++

Add the DJFacet app to your project's ``settings.py``::


	INSTALLED_APPS += (	
		'mptt',             # optional, for hierarchical facets
		'picklefield',      # REQUIRED
		'djfacet',          # REQUIRED
	)

Now run the ``syncdb`` command. DJFacet will create 3 new tables, which are used by the caching system::

	$ python manage.py syncdb
	Creating table djfacet_cachedfacetquery
	Creating table djfacet_cachedfacetvalue
	Creating table djfacet_cachedfacetedmanager



Fianlly, add the DJFacet app to your urls definitions in ``urls.py``::

	urlpatterns += patterns('',
		(r'^browser/', 'djfacet.urls'), # change "browser" to whatever suits you
	)



(Optional) Step 3: Override the templates directory
++++++++++++++++++++++++++++++++++++++++

DJFacets includes several templates, which are located in the /templates folder of the djfacet app. It is likely that you will want to override some (or all) of them. This is easily achieved by copying them into a folder named ``djfacet`` inside your project's ``templates`` directory  (usually defined via Django's ``TEMPLATE_DIRS`` setting).:: 

	$ cd /path/to/my/project/djfacet
	$ cp -r templates/djfacet /path/to/my/project-templates/

Valid templates files found in this location will always take precedence over the ones that come with the DJFacet app. If you copy only some of the templates, make sure you preserve the folder structure.




(Optional) Step 4: Override the media directory
++++++++++++++++++++++++++++++++++++

Do the same operation as above with DJFacet's built-in static files (css, js). Copy the folder named ``djfacet``, located inside the ``static`` of DJFacet distribution, to your project's media folder (usually defined via Django's ``MEDIA_ROOT`` setting)::

	$ cd /path/to/my/project/djfacet
	$ cp -r static/djfacet /path/to/my/project-media-files/

Valid static files files found in this location will always take precedence over the ones that come with the DJFacet app.




Once that works, congratulations! You’ve successfully installed DJFacet. If you run the django server and try to go to 127.0.0.1:8000/browse, you'll see an error in the console. This is ok, because a key component is still missing: the :ref:`configuration` file for the search facets. 

