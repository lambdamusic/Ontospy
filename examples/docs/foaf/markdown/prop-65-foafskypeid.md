Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:skypeID


### Tree


* [foaf:nick](prop-55-foafnick.md)

    * foaf:skypeID





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/skypeID

### Description
&quot;A Skype ID&quot;


### Inherits from (1)

- [foaf:nick](prop-55-foafnick.md)




### Usage


[foaf:Agent](class-4-foafagent.md) 
=&gt;&nbsp;_foaf:skypeID_&nbsp;=&gt;&nbsp;[](.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:skypeID a rdf:Property,<br />        owl:DatatypeProperty ;<br />    rdfs:label &quot;Skype ID&quot; ;<br />    rdfs:comment &quot;A Skype ID&quot; ;<br />    rdfs:domain foaf:Agent ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range rdfs:Literal ;<br />    rdfs:subPropertyOf foaf:nick ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51