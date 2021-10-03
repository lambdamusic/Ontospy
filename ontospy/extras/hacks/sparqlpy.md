Intro
-----------------------------------------
Sparqly is a small python library for querying SPARQL endpoints. It can be used from the command line or as a module in other python applications.

The idea is to make it easy to access sparql endpoints, in a pythonic way.

The main file is a genetic wrapper for any sparql endpoints, providing 4 main methods:
- `query`: accepts a generic query as a string
- `ontology`: queries for all owl:Classes
- `describe`: a describe query for a specific URI
- `alltriples`: a query that returns all the triples mentioning a specific URI

Furthemore, there are two specializations of the main sparql wrapper: nature.py and dbpedia.py.
These are like 'plugins' that embed special behaviour for specific endpoints.

####Dependencies:
Sparqly relies on sparql-wrapper, which itself depends on rdflib. Install both of them using `easy_install`.

- http://sparql-wrapper.sourceforge.net/
- https://github.com/RDFLib


####Credits:
Sparqly main library is based on code found here: http://terse-words.blogspot.co.uk/2012/01/get-real-data-from-semantic-web.html
I just added a few more methods for sparql queries, parametrized the format for the results set etc..





Todo:
-----------------------------------------
- keep on adding queries specific to nature...
- check support for RDF/XML, TURTLE, N3..








ChangeLog:
-----------------------------------------


####19/3/13
- Added verbose option


####7/2/13

- added command line handlers
- added a parameter for convert() [by defaults it's True]
- Added support for JSON and XML formats.







Example (command line)
-----------------------

# getting all classes from the British Museum sparql endpoint

```
[user]:~/code/python/semweb/sparqly>python sparqly.py http://collection.britishmuseum.org/Sparql -q "select ?x where {?x a rdfs:Class}"
Contacting http://collection.britishmuseum.org/Sparql ...
Query: "select ?x where {?x a rdfs:Class}"; Format: JSON

PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
select ?x where {?x a rdfs:Class}


[x] uri=> http://collection.britishmuseum.org/id/crm/E1.CRM_Entity
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E10.Transfer_of_Custody
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E11.Modification
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E12.Production
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E13.Attribute_Assignment
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E14.Condition_Assessment
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E15.Identifier_Assignment
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E16.Measurement
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E17.Type_Assignment
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E18.Physical_Thing
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E19.Physical_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E2.Temporal_Entity
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E20.Biological_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E21.Person
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E22.Man-Made_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E24.Physical_Man-Made_Thing
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E25.Man-Made_Feature
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E26.Physical_Feature
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E27.Site
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E28.Conceptual_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E29.Design_or_Procedure
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E3.Condition_State
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E30.Right
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E31.Document
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E32.Authority_Document
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E33.Linguistic_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E34.Inscription
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E35.Title
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E36.Visual_Item
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E37.Mark
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E38.Image
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E39.Actor
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E4.Period
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E40.Legal_Body
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E41.Appellation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E42.Identifier
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E44.Place_Appellation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E45.Address
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E46.Section_Definition
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E47.Spatial_Coordinates
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E48.Place_Name
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E49.Time_Appellation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E5.Event
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E50.Date
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E51.Contact_Point
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E52.Time-Span
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E53.Place
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E54.Dimension
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E55.Type
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E56.Language
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E57.Material
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E58.Measurement_Unit
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E6.Destruction
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E63.Beginning_of_Existence
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E64.End_of_Existence
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E65.Creation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E66.Formation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E67.Birth
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E68.Dissolution
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E69.Death
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E7.Activity
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E70.Thing
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E71.Man-Made_Thing
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E72.Legal_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E73.Information_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E74.Group
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E75.Conceptual_Object_Appellation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E77.Persistent_Item
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E78.Collection
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E79.Part_Addition
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E8.Acquisition
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E80.Part_Removal
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E81.Transformation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E82.Actor_Appellation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E83.Type_Creation
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E84.Information_Carrier
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E85.Joining
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E86.Leaving
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E87.Curation_Activity
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E89.Propositional_Object
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E9.Move
----
[x] uri=> http://collection.britishmuseum.org/id/crm/E90.Symbolic_Object
----
----------
Time:	   0.17s
Found:	   82
Stats:	   (487/s after 0.17s)
```


# getting all instances of Group from the British Museum sparql endpoint

```
[user]:~/code/python/semweb/sparqly>python sparqly.py http://collection.britishmuseum.org/Sparql -q "select ?p where {?p a <http://collection.britishmuseum.org/id/crm/E74.Group>} limit 10"
Contacting http://collection.britishmuseum.org/Sparql ...
Query: "select ?p where {?p a <http://collection.britishmuseum.org/id/crm/E74.Group>} limit 10"; Format: JSON

PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
select ?p where {?p a <http://collection.britishmuseum.org/id/crm/E74.Group>} limit 10


[p] uri=> http://collection.britishmuseum.org/id/department/A
----
[p] uri=> http://collection.britishmuseum.org/id/department/C
----
[p] uri=> http://collection.britishmuseum.org/id/department/E
----
[p] uri=> http://collection.britishmuseum.org/id/department/G
----
[p] uri=> http://collection.britishmuseum.org/id/department/H
----
[p] uri=> http://collection.britishmuseum.org/id/department/P
----
[p] uri=> http://collection.britishmuseum.org/id/department/W
----
[p] uri=> http://collection.britishmuseum.org/id/department/Y
----
----------
Time:	   0.11s
Found:	   8
Stats:	   (74/s after 0.11s)
[user]:~/code/python/semweb/sparqly>




# using the nature.py command to get the ontology
[user]:~/code/python/semweb/sparqly>python nature.py -o
Contacting http://data.nature.com/sparql ...
Query: ONTOLOGY; Format: JSON

PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX npgx: <http://ns.nature.com/extensions/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
PREFIX prism: <http://prismstandard.org/namespaces/basic/2.1/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX npgg: <http://ns.nature.com/graphs/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX npg: <http://ns.nature.com/terms/>

			SELECT *
			WHERE { ?class a owl:Class }


[class] uri=> http://ns.nature.com/terms/Graph
----
[class] uri=> http://ns.nature.com/terms/Catalog
----
[class] uri=> http://ns.nature.com/terms/Citation
----
[class] uri=> http://ns.nature.com/terms/ProductGroup
----
[class] uri=> http://ns.nature.com/terms/Term
----
[class] uri=> http://ns.nature.com/terms/Subject
----
[class] uri=> http://ns.nature.com/terms/Contributor
----
[class] uri=> http://ns.nature.com/terms/Article
----
[class] uri=> http://ns.nature.com/terms/ProductFamily
----
[class] uri=> http://ns.nature.com/terms/Product
----
[class] uri=> http://ns.nature.com/terms/Publication
----
[class] uri=> http://ns.nature.com/terms/DataCitation
----
[class] uri=> http://ns.nature.com/terms/Coverage
----
[class] uri=> http://ns.nature.com/terms/Technique
----
[class] uri=> http://ns.nature.com/terms/Interest
----
[class] uri=> http://ns.nature.com/terms/Speciality
----
----------
Time:	   1.10s
Found:	   16
Stats:	   (15/s after 1.10s)
[user]:~/code/python/semweb/sparqly>

```







Example (python)
-----------------------


	In [1]: from sparqly import *

	In [2]: s = SparqlEndpoint("http://data.nature.com/sparql")

	In [3]: q = "select ?x where {?x a owl:Class}"

	In [4]: results = s.query(q)
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX void: <http://rdfs.org/ns/void#>
	PREFIX dcterms: <http://purl.org/dc/terms/>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	select ?x where {?x a owl:Class}


	In [5]: print results
	{u'head': {u'vars': [u'x']}, u'results': {u'bindings': [{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Graph'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Catalog'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Citation'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/ProductGroup'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Term'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Subject'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Contributor'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Article'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/ProductFamily'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Product'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Publication'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/DataCitation'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Coverage'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Technique'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Interest'}}, {u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Speciality'}}]}}

	In [6]: for x in results['results']['bindings']:
	   ...:     print x
	   ...:     
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Graph'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Catalog'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Citation'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/ProductGroup'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Term'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Subject'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Contributor'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Article'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/ProductFamily'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Product'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Publication'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/DataCitation'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Coverage'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Technique'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Interest'}}
	{u'x': {u'type': u'uri', u'value': u'http://ns.nature.com/terms/Speciality'}}

	In [7]: results = s.query(q, "XML")
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX void: <http://rdfs.org/ns/void#>
	PREFIX dcterms: <http://purl.org/dc/terms/>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	select ?x where {?x a owl:Class}


	In [8]: print results
	<xml.dom.minidom.Document instance at 0x105333c20>

	In [9]: print results.toxml()
	<?xml version="1.0" ?><sparql xmlns="http://www.w3.org/2005/sparql-results#">
	<head>
	 <variable name="x"/>
	</head>
	<results>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Graph</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Catalog</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Citation</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/ProductGroup</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Term</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Subject</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Contributor</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Article</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/ProductFamily</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Product</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Publication</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/DataCitation</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Coverage</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Technique</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Interest</uri></binding>
	</result>
	<result>
	 <binding name="x"><uri>http://ns.nature.com/terms/Speciality</uri></binding>
	</result>
	</results></sparql>

	In [10]: results = s.query(q, convert=False)
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	PREFIX owl: <http://www.w3.org/2002/07/owl#>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	PREFIX void: <http://rdfs.org/ns/void#>
	PREFIX dcterms: <http://purl.org/dc/terms/>
	PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	select ?x where {?x a owl:Class}



	In [11]: type(results)
	Out[11]: instance

	In [12]: print results
	<SPARQLWrapper.Wrapper.QueryResult instance at 0x10588ee18>

	In [13]: for x in results:
	   ....:     print x
	   ....:     
	{ "head": {"vars": [

	 "x"

	] },

	"results": {

	"bindings": [

		{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Graph"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Catalog"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Citation"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/ProductGroup"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Term"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Subject"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Contributor"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Article"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/ProductFamily"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Product"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Publication"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/DataCitation"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Coverage"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Technique"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Interest"

			}

		},{

			"x": {

			 "type": "uri",

			 "value": "http://ns.nature.com/terms/Speciality"

			}

		}

	] } }


	In [14]: results.info()
	Out[14]:
	{'connection': 'close',
	 'content-length': '1541',
	 'content-type': 'application/sparql-results+json',
	 'date': 'Thu, 07 Feb 2013 16:35:51 GMT',
	 'server': 'Jetty(6.1.26)',
	 'set-cookie': 'BIGipServerjetty-external=rd1o00000000000000000000ffff0a0101cbo80; expires=Thu, 07-Feb-2013 17:35:51 GMT; path=/',
	 'x-cerberus-query-processing-time': '0.282',
	 'x-cerberus-version-number': '1.4.0'}
