Introduction
************************
In this section we introduce the main features of DJFacet and the concept of faceted search. 


What are dynamic taxonomies systems?
==============================================================

Dynamic taxonomies systems, also known as faceted search systems, are one of the most recent advances in search interfaces of the last years.  In a nutshell, this approach allows users to explore a collection of information by *incrementally adding* or *removing* filters representing concepts that describe the information available.

Dynamic taxonomies systems are currenlty used by dozens of web applications in e-commerce, e-government, cultural heritage and various other sectors. 

An introductory article on `A List Apart <http://www.alistapart.com/articles/design-patterns-faceted-navigation/>`_ describes faceted search as follows:

.. topic:: A definition:

   The faceted navigation model leverages metadata fields and values to provide users with visible options for clarifying and refining queries. Faceted navigation [...] features an integrated, incremental search and browse experience that lets users begin with a classic keyword search and then scan a list of results. It also serves up a custom map (usually to the left of results) that provides insights into the content and its organization and offers a variety of useful next steps. That’s where faceted navigation proves its power. In keeping with the principles of progressive disclosure and incremental construction, users can formulate the equivalent of a sophisticated Boolean query by taking a series of small, simple steps.

This `mindmap <http://www.michelepasin.org/techblog/2009/03/05/faceted-browsing-a-conceptual-map/>`_ provides a lot more information about existing faceted browsers and the principles behind them. You do not need all this theory in order to set up DJFacet, but skimming through it might turn out to be useful for you. Alternatively, check out the :ref:`learning` section at the bottom of this page.


Features of DJFacet
====================

There are several faceted search systems out there, which vary a great degree in terms of the language they're written in, the back-ends supported and obviously the user interface capabilities (wikipedia maintains an `extensive list <http://en.wikipedia.org/wiki/Faceted_search>`_ of them). 

DJFacet is entirely dependent on the Django Python framework, so if you're using other environments unfortunately you won't be able to enjoy the many features of DJFacet, which are: 

Simplicity
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
DJFacet has been designed so to be easy-to-use: installation and integration with existing Django projects doesn't require more than a couple of hours, provided you've understood the principles behind the facets configuration.
	

Back-end agnostic
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
DJFacet rests on Django's Database API, which provides a layer of abstraction between the raw SQL and Python. A number of relational databases are supported (`click here <https://docs.djangoproject.com/en/1.3/ref/settings/#engine>`_ to see a list). Even when other back-ends will be added in the future, DJFacet is guaranteed to keep working.


Minimal look&feel
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
The user interface that comes by default with DJFacet is purposely minimal and thus easily modifiable. The search templates, organized via inheritance and inclusion mechanisms, can be singularly overridden when necessary.


REST architecture
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
DJFacet supports a REST architecture: every item in your database is represented uniquely using a deterministic algorithm. Moreover, every search page generates a unique url, thus your users can easily create bookmarks and use the browser's back button.


It supports pivoting 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Most faceted search systems available let you search for *one object-type* only (e.g., *cars*, or *products*), by manipulating facets representing some of its key features (e.g., *color*, *price*). If your information space is more complex, you might want to be able to use the facets to narrow down different *types* of result sets. For example, a bibliographical faceted search system could let users use the 'publication-date' facet when searching for *books* or for *authors*. 
The technical term for this functionality is *pivoting*, and is a quite advanced feature in faceted search systems. In a nutshell, the type of objects being searched for can be *changed dynamically* while keeping the currently selected search options. As a results, you are effectively changing the main *perspective* (the *pivot*) of a search. This is possible because when the objects being searched for map to tables (i.e., Django models) that are connected in the database, we can use that connection to generate a new query. DJFacets architecture lets you define as many pivots as you like, just by adding a few extra lines of code.


It has a caching system 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
If the facets generated from your database have a large number of terms (also called *zoom points*) and you have several of these query-intensive facets, the loading time of the search interface could increase too much. To address this problem, DJFacet provides a dedicated caching system. By using a management command, you can pre-load all the facets and cache them for a quicker recollection when needed. 


It's still being improved...
++++++++++++++++++++++++++++++
DJFacet has various other features (hierarchical facets, custom facets) that are still in the making. Stay tuned for more!



.. _keyterms:

Key terms
====================
The following list provides some definitions for the most common concepts used in faceted search systems.

Taxonomy
++++++++++
A taxonomy, or taxonomic scheme, is a particular classification ("the taxonomy of ..."), arranged in a **hierarchical** structure. Typically this is organized by supertype-subtype relationships, also called generalization-specialization relationships, or less formally, parent-child relationships.

Dynamic Taxonomy
+++++++++++++++++
Dynamic taxonomies (DT, also recently known as **faceted search systems**) are a general knowledge management model based on a multidimensional classification of heterogeneous data objects and are used to explore/browse complex information bases in a guided yet unconstrained way through a visual interface. The model is primarily concerned with user-centered access, and object classification is not addressed in the base model.

Facet
+++++++
A facet comprises "clearly defined, mutually exclusive, and collectively exhaustive aspects, properties or characteristics of a class or specific subject". For example, a collection of books might be classified using an **author** facet, a **subject** facet, a **date** facet, etc.

Facet-Value
++++++++++++++	
A single entity within a facet; for example, the entity '**history**' within the **subject** facet. Facet-values are also known as *concepts*, *terms*, *zoom points* or *filters*.

Facets-Group
++++++++++++++
A set of facets which are grouped together because they share some intrinsic feature. For example, the **author** facet and **publication-date** facet can be grouped in the **publication-information** facet-group. 


Zooming in/out
+++++++++++++++++++++
The action of narrowing/broadening a search space by selecting/deselecting facet-values. 




.. _learning:

Other learning resources
=========================

If you want to learn more about the theory and applications of faceted search systems, the resources listed below may be of help.

**Introductory** materials:

- `Design Patterns: Faceted Navigation <http://www.alistapart.com/articles/design-patterns-faceted-navigation/>`_. An online article on http://www.alistapart.com/

- `Use of Faceted Classification <http://www.webdesignpractices.com/navigation/facets.html>`_. An online article on http://www.webdesignpractices.com


More **advanced** resources:

- `Dynamic Taxonomies and Faceted Search <http://www.springer.com/computer/database+management+&+information+retrieval/book/978-3-642-02358-3>`_, Sacco, Giovanni Maria; Tzitzikas, Yannis (Eds.), Springer, 2009. This book contains an in-depth analysis of all aspects of dynamic taxonomies.

- `Putting Facets on the Web: An Annotated Bibliography <http://www.miskatonic.org/library/facet-biblio.html>`_. An online bibliography by Miskatonic University Press

