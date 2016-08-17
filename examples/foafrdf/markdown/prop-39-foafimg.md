Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:img


### Tree


* [foaf:depiction](prop-25-foafdepiction.md)

    * foaf:img





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/img

### Description
&quot;An image that can be used to represent some thing (ie. those depictions which are particularly representative of something, eg. one&#39;s photo on a homepage).&quot;


### Inherits from (1)

- [foaf:depiction](prop-25-foafdepiction.md)




### Usage


[foaf:Person](class-14-foafperson.md) 
=&gt;&nbsp;_foaf:img_&nbsp;=&gt;&nbsp;[foaf:Image](class-7-foafimage.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:img a rdf:Property,<br />        owl:ObjectProperty ;<br />    rdfs:label &quot;image&quot; ;<br />    rdfs:comment &quot;An image that can be used to represent some thing (ie. those depictions which are particularly representative of something, eg. one&#39;s photo on a homepage).&quot; ;<br />    rdfs:domain foaf:Person ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range foaf:Image ;<br />    rdfs:subPropertyOf foaf:depiction ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51