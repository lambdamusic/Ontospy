Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:mbox


### Tree

* rdfs:Property
    * foaf:mbox





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/mbox

### Description
&quot;A  personal mailbox, ie. an Internet mailbox associated with exactly one owner, the first owner of this mailbox. This is a &#39;static inverse functional property&#39;, in that  there is (across time and change) at most one individual that ever has any particular value for foaf:mbox.&quot;


### Inherits from:
owl:Thing



### Usage


[foaf:Agent](class-4-foafagent.md) 
=&gt;&nbsp;_foaf:mbox_&nbsp;=&gt;&nbsp;[](.md)

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:mbox a rdf:Property,<br />        owl:InverseFunctionalProperty,<br />        owl:ObjectProperty ;<br />    rdfs:label &quot;personal mailbox&quot; ;<br />    rdfs:comment &quot;A  personal mailbox, ie. an Internet mailbox associated with exactly one owner, the first owner of this mailbox. This is a &#39;static inverse functional property&#39;, in that  there is (across time and change) at most one individual that ever has any particular value for foaf:mbox.&quot; ;<br />    rdfs:domain foaf:Agent ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:range owl:Thing ;<br />    vs:term_status &quot;stable&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51