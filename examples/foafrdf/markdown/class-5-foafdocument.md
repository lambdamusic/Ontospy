Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Class foaf:Document


### Tree

* OWL:Thing
    * foaf:Document


        * [foaf:Image](class-7-foafimage.md) 

        * [foaf:PersonalProfileDocument](class-15-foafpersonalprofiledocument.md) 
        






### URI
http://xmlns.com/foaf/0.1/Document

### Description
&quot;A document.&quot;



### Inherits from:
owl:Thing




### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:Document a rdfs:Class,<br />        owl:Class ;<br />    rdfs:label &quot;Document&quot; ;<br />    rdfs:comment &quot;A document.&quot; ;<br />    rdfs:isDefinedBy foaf: ;<br />    owl:disjointWith foaf:Organization,<br />        foaf:Project ;<br />    vs:term_status &quot;testing&quot; .</p>

<p></p>
```




### Instances of foaf:Document can have the following properties:

<table border="1" cellspacing="3" cellpadding="5" class="classproperties table-hover ">

    <tr>
        <th height="40">Property</th><th>Description</th><th>Expected Type</th>
    </tr>

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:primaryTopic" href="prop-61-foafprimarytopic.md">foaf:primaryTopic</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The primary topic of some page or document.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:sha1" href="prop-64-foafsha1.md">foaf:sha1</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A sha1sum hash, in hex.&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:topic" href="prop-72-foaftopic.md">foaf:topic</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A topic of some page or document.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            

        

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="owl:Thing" href="class-0-owlthing.md" class="rdfclass">owl:Thing</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:dnaChecksum" href="prop-27-foafdnachecksum.md">foaf:dnaChecksum</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A checksum for the DNA of some thing. Joke.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:givenName" href="prop-35-foafgivenname.md">foaf:givenName</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The given name of some person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:membershipClass" href="prop-51-foafmembershipclass.md">foaf:membershipClass</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Indicates the class of individuals that are a member of a Group&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:nick" href="prop-55-foafnick.md">foaf:nick</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A short informal nickname characterising an agent (includes login identifiers, IRC and other chat nicknames).&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:phone" href="prop-59-foafphone.md">foaf:phone</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A phone,  specified using fully qualified tel: URI scheme (refs: http://www.w3.org/Addressing/schemes.html#tel).&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:title" href="prop-71-foaftitle.md">foaf:title</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Title (Mr, Mrs, Ms, Dr. etc)&quot;</span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="dc:date" href="prop-78-dcdate.md">dc:date</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="dc:description" href="prop-79-dcdescription.md">dc:description</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="dc:title" href="prop-80-dctitle.md">dc:title</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="vs:term_status" href="prop-81-vsterm_status.md">vs:term_status</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="wot:assurance" href="prop-82-wotassurance.md">wot:assurance</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="wot:src_assurance" href="prop-83-wotsrc_assurance.md">wot:src_assurance</a>         
                </td>
                <td class="thirdtd">
                    <span></span>
                </td>
                <td class="secondtd">
                    
                        <i>owl:Thing</i>
                    
                </td>
            </tr>

            

        

    

</table>













---

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on 18th August 2016 00:51