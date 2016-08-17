Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Property foaf:nick


### Tree

* rdfs:Property
    * foaf:nick


        * [foaf:aimChatID](prop-21-foafaimchatid.md) 

        * [foaf:icqChatID](prop-38-foaficqchatid.md) 

        * [foaf:msnChatID](prop-52-foafmsnchatid.md) 

        * [foaf:skypeID](prop-65-foafskypeid.md) 

        * [foaf:yahooChatID](prop-77-foafyahoochatid.md) 
        






### URI
http://xmlns.com/foaf/0.1/nick

### Description
&quot;A short informal nickname characterising an agent (includes login identifiers, IRC and other chat nicknames).&quot;


### Inherits from:
owl:Thing



### Usage
owl:Thing=&gt;&nbsp;_foaf:nick_&nbsp;=&gt;&nbsp;owl:Thing

### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:nick a rdf:Property,<br />        owl:DatatypeProperty ;<br />    rdfs:label &quot;nickname&quot; ;<br />    rdfs:comment &quot;A short informal nickname characterising an agent (includes login identifiers, IRC and other chat nicknames).&quot; ;<br />    rdfs:isDefinedBy foaf: ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```










---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51