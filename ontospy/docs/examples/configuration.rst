.. _configuration:

Configuration
************************

Once you've installed DJFacet, the final step before having a fully-working faceted browser is  the definition of the facets that can be used for searching an information space. 

This involves three steps: 

1. Defining an *information space*.
2. Defining the *facet-groups*.
3. Defining the *facets* appearance and behaviour, with respect to the information space.

The configuration file is a standard python module, whose location is defined by the :ref:`DJF_SPECS_MODULE` setting (by default, DJFacet will look for a file called ``facetspecs.py`` at the root of your django project).  


Defining the information space
=======================================

The information space is represented through a list of dictionaries, in a variable called ``result_types``. Each element of the list defines a valid result-type. 

For example, in our demo application (link) we want users to be able to search for either *Religions* or *Countries*, so our information space is composed by two elements::

	from myapp.mymodels import Religion, Countries
	
	result_types = [{	'label' : 'Religions', 
				'uniquename' : 'religions', 
				'infospace' : Religion	,
				'isdefault' : True    },
						
			{	'label' : 'Countries', 
				'uniquename' : 'country',  
				'infospace' : Country,
			}]


.. _infospaceoptions:

Information space options
=======================================

The options passed in the ``result_types`` dictionary serve to define the main features of a result type. 

``label``
++++++++++++++
Required: Yes

The string used in the interface as the heading for this result type. Usually a nice version of the ``'uniquename'`` parameter.

``uniquename``
+++++++++++++++++++
Required: Yes

A string used internally as a unique name for this specific result type.


``infospace``
++++++++++++++++++
Required: Yes

A Django model, or a queryset. This determines the maximum set of results for a possible result-type. For example, if set to ``Religion``, it entails that the beginning of our query is equivalent to the queryset obtained by executing ``Religion.objects.all()``.


``isdefault``
++++++++++++++++++
Required: No

Determines whether a result-type needs to be used as the default one when the faceted browser is loaded. It defaults to False.


.. _defininggroups:

Defining the facet-groups
=======================================

The facet-groups are essentially containers of facets. They are mostly used for display purposes, as they let you organize the facets available in a way that is more understandable by users.

Facet-groups are represented through a list of dictionaries, in a variable called ``facet_groups``. Each element of the list defines a valid facet-group. 

For example, in our demo application has facets conceptualising features of places (e.g., *country names*) and facets conceptualising features of religions (e.g., *religion names*). Thus we decided to create two facet-groups::
	
	facet_groups = [{	'label':	'Place Descriptors', 
				'position': 1,
				'uniquename' :	'countrygroup', 
				'default' : True   } ,
						
			{	'label':	'Religion Descriptors', 
				'position': 2,
				'uniquename' :	'religiongroup', 
				'default' : True   
			}]

.. note:: 
	Even if you do not want to have multiple groups, DJFacet expects you to define at least one group and attach all the facets to it.

.. _facetgroupoptions:

Facet-groups options
=======================================

``label``
++++++++++++++
Required: Yes

The string used in the interface as the heading for this facet-group. Usually a nice version of the ``'uniquename'`` parameter.

``uniquename``
+++++++++++++++++++
Required: Yes

A string used internally as a unique name for this specific facet-group.


``position``
++++++++++++++++++
Required: No

A number used for ordering the facet-groups list in the interface. The one with the lowest position is displayed at the top. 


``default``
++++++++++++++++++
Required: No

[DOUBLE CHECK] Determines whether a facet-group is used or not. It defaults to False.(?)


.. _definingfacets:

Defining the facets
=======================================

The facets are represented through a variable names ``facetslist``, which is a list of dictionaries. Each dictionary describes a facet by defining **appearance** parameters and **behaviour** parameters. 

These two parameters are themselves organized using dictionaries and lists of dictionaries, so the abstract structure of the ``facetslist`` variable will end up looking like this::


	facetslist = [   # FACET-1
			{'appearance' 	: { 'label' : '...' ,  'another_parameter' : '...' , 	} ,
			 'behaviour' 	: [{ 'resulttype1' : 'some behaviour', },
					   { 'resulttype2' : 'another behaviour', },
					]},   
					# ... end of facet-1
			# FACET-2
			{'appearance' 	: { 'label' : '...' ,  'another_parameter' : '...' , 	} ,
			 'behaviour' 	: [{ 'resulttype1' : 'some behaviour', },
					   { 'resulttype2' : 'another behaviour', },
					]},   
					# ... end of facet-2
			# ... etc....
				]

Let's now have a look at the defining parameters for each facet in more details.  

The **appearance** parameter is a dictionary containing information on how to create and display the facet and its contents. In general, a facet is derived from one of the models available in your application; more precisely, a facet derives from one of the properties (= usually corresponding to columns in the DB table) of a model. All the possible values of that property are thus retrieved and used to populate the contents of a facet. Each of these values will then be used for creating queries. 

Besides specifying what model property the facet derives from, in the **appearance** dictionary we must also specify other characteristics of the facet, such as its pretty-name and which group it belongs too (see the section below for more details)::

	{'appearance' : {	
			'label' : 'Region name' , 
			'uniquename' : 'regionname',
			'model' : Region , 
			'dbfield' : "name", 
			'displayfield' : "name", 
			'explanation': "no explanation yet",
			'grouping'	: ['countrygroup'],
			'ordering' : 'extended_name',
			} 
		}

								
				
The **behaviour** parameter is a list of dictionaries containing information about the specific query that needs to be carried out once a facet-value is chosen. The query is specified using Django's *underscore* syntax. Note that since we can have multiple result-types defined in our information space (see above), in principle we can have *as many behaviours as the result-types we defined*. This is the main mechanism behind the *pivoting* feature of DJFacet (as described in the introduction).

In other words, each facet will differently contribute to the creation of a query depending on whether we're searching for objects of type X (e.g., *countries*) or Y (e.g., *religions*). In order for this to be possible, each of the querypaths need to be specified explicitly in the **behaviour** dictionary (alongside other information useful for describing the query). So for example, in our demo application the 'Region name' facet can be used when searching for *countries*, or when searching for *religions*::


	{ 'behaviour' :  [{
			'resulttype' : 'religions',
			'querypath' : 'country__inregion__name', 
			'inversepath' : None,
			'explanation' : "showing all religions in selected region (through associated countries)" 
				},
			{
			'resulttype' : 'country',
			'querypath' : 'inregion__name', 
			'inversepath' : None,
			'explanation' : "showing all countries in selected region" 
				},
			]}


Now we can put together the two parameters definitions above, so to obtain the entire facet definition for the 'Region name' facet. Check out the following sections in order to find out more about the available parameters for describing facets::

	facetslist = [  
			{	'active' : True,
				'appearance' : {	
					'label' : 'Region name' , 
					'uniquename' : 'regionname',
					'model' : Region , 
					'dbfield' : "name", 
					'displayfield' : "name", 
					'explanation': "no explanation yet",
					'grouping'	: ['countrygroup'],
					'ordering' : 'extended_name',
						} ,
				'behaviour' :  [{
					'resulttype' : 'religions',
					'querypath' : 'country__inregion__name', 
					'inversepath' : None,
					'explanation' : "showing all...." 
						},
					{
					'resulttype' : 'country',
					'querypath' : 'inregion__name', 
					'inversepath' : None,
					'explanation' : "showing all...." 
						},
					]},  
				]


.. _genericoptions:

Generic options
=======================================	

``active``
++++++++++++++
Required: No / Default: True

Specifies if a facet needs to be loaded. Can be used as a quick on/off switch for adding/removing facets. Defaults to True, so it can be omitted safely. 


.. _facetappearanceoptions:

Facet Appearance options
=======================================	
					
``label``
++++++++++++++
Required: Yes

The string used in the interface as the heading for this facet. Usually a nice version of the ``'uniquename'`` parameter.


``uniquename``
+++++++++++++++++++
Required: Yes

A string used internally as a unique name for this specific facet-group.

``grouping``
++++++++++++++++++++++++++++
Required: Yes

A list indicating which facet-groups this facet belongs to. The list should contain at least one of the previously defined facet-groups, using its ``uniquename`` (as described in the :ref:`facetgroupoptions` section above).


``dbfield``
++++++++++++++++++++++++++++
Required: Yes

The name of the field in a Django model that we want to use for generating the inner values of a facet. For example, if the *author* facet derives from a model called *Person*, and this model has a *person_name* string field, we can use *person_name* to generate the facet-values for the *author* facet. The *person_name* values are thus what is being used in the faceted browser queries. 


``displayfield``
++++++++++++++++++++++++++++
Required: No

A field in a Django model that is used only for display purposes within a facet, instead of the corresponding ``dbfield`` value. For example, if the *author* facet derives from a model called *Person*, and this model has a *person_name* string field alongside a *person_nicename* string field, we can use *person_nicename* to generate the visible facet-values for the *author* facet (by setting it as the ``displayfield``), and *person_name* to run the queries (by setting it as the ``dbfield``). Note that a ``displayfield`` always needs to be accompanied by a ``dbfield``.


``ordering``
++++++++++++++++++++++++++++
Required: No

A field in the Django model a facet derives from, which should be used for ordering the facet-values. If not provided, the default ordering of the model is used.


``explanation``
++++++++++++++++++++++++++++
Required: No

A natural language description, which can be used for example to help users understand the meaning of a facet.


..
    THIS IS A COMMENT
	``hierarchy``
	++++++++++++++++++++++++++++
	Required: ??

	A .....



.. _facetbehaviouroptions:

Facet Behaviour options
=======================================	
					
``resulttype``
++++++++++++++++++++++++++++
Required: Yes

A string indicating which result-type this behaviour applies to. This string should match one of the previously defined result-types (as part of the information space, check the :ref:`infospaceoptions` section above) using its ``uniquename`` value.


``querypath``
++++++++++++++++++++++++++++
Required: Yes

The querypath used to calculate a query, for a specific ``resulttype``. This value is expressed using Django's `double underscore syntax <https://docs.djangoproject.com/en/1.3/topics/db/queries/#field-lookups>`_, which translates into field lookups analogue to a SQL WHERE clause. 

Finding this value in some cases is not straightforward, and it is useful to test the query in the shell in order to get it right (especially with inverse relations). Keep in mind that the querypath should be the full string used in a query that goes from the result-type to the facet ``dbname`` in question. 



``inversepath``
++++++++++++++++++++++++++++
Required: No

The querypath used to refresh the contents of the available facets, after a zoom-in or zoom-out query has been completed. Normally, it is not necessary to set this value explicitly, because DJFacet infers it using the information in your models and the ``querypath`` value. If you feel that the inference mechanism is failing to get the right inverse relation, you might want to set this value explicitly and override DJFacet standard behaviour.


``explanation``
++++++++++++++++++++++++++++
Required: No

A natural language description, which can be retrieved dynamically to used to help users understand the meaning of a query (as the result of combining a facet with a specific result-type).
