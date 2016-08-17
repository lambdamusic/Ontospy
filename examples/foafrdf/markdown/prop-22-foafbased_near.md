Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:based_near


### Tree

* rdfs:Property
    * foaf:based_near





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/based_near

### Description
&quot;A location that something is based near, for some broadly human notion of near.&quot;


### Inherits from:
owl:Thing



### Usage


[http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing](class-3-httpwwww3org200301geowgs84_posspatialthing.md) 
=&gt;&nbsp;_foaf:based_near_&nbsp;=&gt;&nbsp;[http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing](class-3-httpwwww3org200301geowgs84_posspatialthing.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:based_near a rdf:Property,<br />        owl:ObjectProperty ;<br />    rdfs:label &quot;based near&quot; ;<br />    rdfs:comment &quot;A location that something is based near, for some broadly human notion of near.&quot; ;<br />    rdfs:domain &lt;http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing&gt; ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range &lt;http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing&gt; ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51