.. _settings:

Settings options
************************

DJFacet can be customised by setting a number of predefined variables in your ``settings.py`` file.  

.. note::
	If you do not set this variables explicitly, they'll get a default value as specified below (which in most situations will work just fine).


.. _DJF_SPECS_MODULE:

DJF_SPECS_MODULE
++++++++++++++++

Defaults to ``'facetspecs'``. 

It determines what file name the configuration file has, and where it is located. 

By default, DJFacet expects to find the configuration file (``facetspecs.py``) at the root of your django project, that is, where your ``setting.py`` file is. In general, you shouldn't need to change this setting.	


.. _DJF_SHOWLOGS:

DJF_SHOWLOGS
++++++++++++++

Defaults to ``False``. 

It determines whether the logs DJFacet produces should be printed out in the shell. This is useful in development mode, to see what's going on when facets are created and populated.


.. _DJFACET_COUNT:

DJFACET_COUNT
++++++++++++++

Defaults to ``True``. 

It determines whether the count for the  *zoom-points* in the facets must be calculated, or not. 

If your application has a lot of data (and facets), setting this value to False can be useful for testing, since it will speed up considerably the refresh operation.  


.. _DJF_CACHE:

DJF_CACHE
++++++++++++++

Defaults to ``False``. 

It determines whether the Cache is used or not. 

Once the cache is activated, DJFacet will always attempt to refresh the facets using the values stored in the database, instead of calculating them each time. Note that if the system detects unsaved objects, it caches them on-the-fly. Alternatively, you can cache all facets-contents using the appropriate management command (see the :ref:`management` section).

.. warning::
	If this parameter is set to True, you must have created the *cached Faceted-Manager* object using the appropriate management command (see the :ref:`management` section). 


.. _DJF_AJAX:

DJF_AJAX
++++++++++++++

Defaults to ``False``. 

It determines whether the user interface should update the facets values asynchronously, or not. 

If set to True, each of the facets in your search interface will become an html ``<div>`` element that can be opened or close. When opened, the back-end is called and its contents are refreshed via ajax.


.. _DJF_MAXRES_PAGE:

DJF_MAXRES_PAGE
++++++++++++++++++++++++++++

Defaults to ``50``. 

It determines the max number of results that a faceted search should display. The rest of the results will be paginated accordingly (see the :ref:`templates` section for more details).




.. _DJ_2COLUMNS_INNERFACET:

DJ_2COLUMNS_INNERFACET [REMOVED!]
++++++++++++++++++++++++++++

Defaults to ``False``. 

It determines whether the two-columns html template should be used for rendering the list of terms within a facet (see the :ref:`templates` section for more details).






