Demo application
************************

- the example app already contains djfacet
- all the source code for the application can be found here (in this tutorial we'll be building it incrementally)
- a running version of the application can be found here: www.michelepasin.org/software/demo/djfacet


Prerequisites
=============
- django, sqllite or sql
- download the models definitions
- download the data

The religions DB has this schema

.. link to the image! 


Installation
============

- run python syncdb and create the SQLlite database

- import the data (explain how I got the data )::

	bash-3.2$ python manage.py loaddata religions.json
	Installing json fixture 'religions' from '/Your/path/to/djfacet_test/religions/fixtures'.
	Installed 1596 object(s) from 1 fixture(s)



- now open up a browser, go to http://127.0.0.1:8000/ [show image]

- enter the admin and have a look at the data; essentially the data model we have is this: 

Country  ... hasMany .... REligions
Religion ... hasOne .... Country

etc...

Check the models.py file for more info


Setting up DJFacet
==================

- creating the facetspecs.py file

- adding a URL handler 

- now open up a browser, go to http://127.0.0.1:8000/djfacet/ [show image]



Customizing the faceted browser
===============================

- polishing up the facetespecs

- Adding and modifying the templates


Other info
===========

- turning on the debug

- turning on the ajax facets








