.. _management:

Management commands
************************

This section is not available yet (but it'll be soon). Stay tuned!


PS: for the cache to work you need to run both the 'djfacet_fmcache' command and the 'djfacet_facetcache' command! 

If you run only the first one it throws an error.. shouldnit be caching on the fly? TODO




djfacet_shell
=======================================

# bash-3.2$ python manage.py djfacet_shell

#  This command loads a shell with added the following symbols:
#  	 'loaded_facet_groups' = ..
#	 'facets_for_template' = ..			
#	 'result_types' = ..			
#	 'fm' = faceted manager instance
#
##################

Creates...





djfacet_fmcache
=======================================


##################
#  Tue Sep 14 15:29:58 CEST 2010
#	THis command needs to be run BEFORE using the DB cache functionalities on the browser!!!!
#
##################


# EG:
# bash-3.2$ python manage.py djfacet_fmcache

Creates...  each time the fm cache is created the previous one is deleted automatically (so no need to pre-delete anything)

Mind that after creating the cache you must set DJF_CACHE = True in order to use it 



djfacet_facetcache
=======================================

# EG:
# bash-3.2$ python manage.py djfacet_facetcache
# bash-3.2$ python manage.py djfacet_facetcache gender
# bash-3.2$ python manage.py djfacet_facetcache gender --secondlevel=yes  --lowerlimit=9905
# bash-3.2$ python manage.py djfacet_facetcache possoffice possunfreepersons posslands possrevkind possrevsilver privileges


make_option('--resulttypes', action='store', dest='resulttypes', default='all',
			help='The _resulttypes_ option determines what resulttypes-facet couple will be cached'),
make_option('--enforce', action='store', dest='enforce', default='yes',
			help='The _enforce_ option determines whether we delete previously cached object (default= TRUE!)'),
make_option('--onlyrescounts', action='store', dest='onlyrescounts', default='no',
			help='The _onlyrescounts_ option determines whether to update only the res tot-counts (no facet values)'),
make_option('--fmcache', action='store', dest='fmcache', default='no',
			help='The _fmcache_ option determines whether to recache the faceted manager instance too'),


Creates...




djfacet_cleanhtmlcache
=======================================

# EG:
# bash-3.2$ python manage.py djfacet_cleanhtmlcache 


Delete CachedHtmlPage objects so that it gets re-calculated


If 'DJF_SPLASHPAGE_CACHE' is set to True the all-facets page will be cached again automatically the first time they're loaded.



djfacet_cleanfacetcache
=======================================

# EG:
# bash-3.2$ python manage.py djfacet_cleanfacetcache surname

option_list = BaseCommand.option_list  + (
					make_option('--resulttypes', action='store', dest='resulttypes', default='all',
								help='The _resulttypes_ option determines what resulttypes-facet couple will be cached'),
					make_option('--emptyunused', action='store', dest='emptyunused', default='no',
								help='The _emptyunused_ option empties the unused elements from CachedFacetValue and CachedQueryArgs tables'),
					make_option('--firstlevel', action='store', dest='firstlevel', default='no',
								help='The _firstlevel_ option determines whether we delete only objects at the firstlevel (= with no QueryArgs)'),
					make_option('--secondlevel', action='store', dest='secondlevel', default='no',
								help='The _secondlevel_ option determines whether to delete only objects at the firstlevel (= with QueryArgs)'),
			  )



Deletes...




