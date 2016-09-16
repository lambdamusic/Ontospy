Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:depiction


### Tree

* rdfs:Property
    * foaf:depiction


        * [foaf:img](prop-39-foafimg.md) 
        






### URI
http://xmlns.com/foaf/0.1/depiction

### Description
&quot;A depiction of some thing.&quot;


### Inherits from:
owl:Thing



### Usage


[](.md) 
=&gt;&nbsp;_foaf:depiction_&nbsp;=&gt;&nbsp;[foaf:Image](class-7-foafimage.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:depiction a rdf:Property,<br />        owl:ObjectProperty ;<br />    rdfs:label &quot;depiction&quot; ;<br />    rdfs:comment &quot;A depiction of some thing.&quot; ;<br />    rdfs:domain owl:Thing ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range foaf:Image ;<br />    owl:inverseOf foaf:depicts ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51