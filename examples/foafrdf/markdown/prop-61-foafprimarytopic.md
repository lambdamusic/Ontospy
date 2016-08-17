Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:primaryTopic


### Tree

* rdfs:Property
    * foaf:primaryTopic





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/primaryTopic

### Description
&quot;The primary topic of some page or document.&quot;


### Inherits from:
owl:Thing



### Usage


[foaf:Document](class-5-foafdocument.md) 
=&gt;&nbsp;_foaf:primaryTopic_&nbsp;=&gt;&nbsp;[](.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:primaryTopic a rdf:Property,<br />        owl:FunctionalProperty,<br />        owl:ObjectProperty ;<br />    rdfs:label &quot;primary topic&quot; ;<br />    rdfs:comment &quot;The primary topic of some page or document.&quot; ;<br />    rdfs:domain foaf:Document ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range owl:Thing ;<br />    owl:inverseOf foaf:isPrimaryTopicOf ;<br />    vs:term_status &quot;stable&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51