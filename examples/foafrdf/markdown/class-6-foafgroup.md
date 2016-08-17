Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Class foaf:Group


### Tree


* [foaf:Agent](class-4-foafagent.md)

    * foaf:Group





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/Group

### Description
&quot;A class of Agents.&quot;



### Inherits from (1)

- [foaf:Agent](class-4-foafagent.md)





### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:Group a rdfs:Class,<br />        owl:Class ;<br />    rdfs:label &quot;Group&quot; ;<br />    rdfs:comment &quot;A class of Agents.&quot; ;<br />    rdfs:subClassOf foaf:Agent ;<br />    vs:term_status &quot;stable&quot; .</p>

<p></p>
```




### Instances of foaf:Group can have the following properties:

<table border="1" cellspacing="3" cellpadding="5" class="classproperties table-hover ">

    <tr>
        <th height="40">Property</th><th>Description</th><th>Expected Type</th>
    </tr>

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="foaf:Group" href="class-6-foafgroup.md" class="rdfclass">foaf:Group</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:member" href="prop-50-foafmember.md">foaf:member</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Indicates a member of a Group&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Agent" href="class-4-foafagent.md" class="rdfclass">foaf:Agent</a>

                    
                    
                </td>
            </tr>

            

        

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="foaf:Agent" href="class-4-foafagent.md" class="rdfclass">foaf:Agent</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:account" href="prop-17-foafaccount.md">foaf:account</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Indicates an account held by this agent.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:OnlineAccount" href="class-9-foafonlineaccount.md" class="rdfclass">foaf:OnlineAccount</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:age" href="prop-20-foafage.md">foaf:age</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The age in years of some agent.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:aimChatID" href="prop-21-foafaimchatid.md">foaf:aimChatID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;An AIM chat ID&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:birthday" href="prop-23-foafbirthday.md">foaf:birthday</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The birthday of this Agent, represented in mm-dd string form, eg. &#39;12-31&#39;.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:gender" href="prop-34-foafgender.md">foaf:gender</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The gender of this Agent (typically but not necessarily &#39;male&#39; or &#39;female&#39;).&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:holdsAccount" href="prop-36-foafholdsaccount.md">foaf:holdsAccount</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Indicates an account held by this agent.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:OnlineAccount" href="class-9-foafonlineaccount.md" class="rdfclass">foaf:OnlineAccount</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:icqChatID" href="prop-38-foaficqchatid.md">foaf:icqChatID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;An ICQ chat ID&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:interest" href="prop-40-foafinterest.md">foaf:interest</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A page about a topic of interest to this person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:jabberID" href="prop-42-foafjabberid.md">foaf:jabberID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A jabber ID for something.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:made" href="prop-46-foafmade.md">foaf:made</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;Something that was made by this agent.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:mbox" href="prop-48-foafmbox.md">foaf:mbox</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A  personal mailbox, ie. an Internet mailbox associated with exactly one owner, the first owner of this mailbox. This is a &#39;static inverse functional property&#39;, in that  there is (across time and change) at most one individual that ever has any particular value for foaf:mbox.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:mbox_sha1sum" href="prop-49-foafmbox_sha1sum.md">foaf:mbox_sha1sum</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The sha1sum of the URI of an Internet mailbox associated with exactly one owner, the  first owner of the mailbox.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:msnChatID" href="prop-52-foafmsnchatid.md">foaf:msnChatID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;An MSN chat ID&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:openid" href="prop-56-foafopenid.md">foaf:openid</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;An OpenID for an Agent.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:skypeID" href="prop-65-foafskypeid.md">foaf:skypeID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A Skype ID&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:status" href="prop-66-foafstatus.md">foaf:status</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A string expressing what the user is happy for the general public (normally) to know about their current activity.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:tipjar" href="prop-70-foaftipjar.md">foaf:tipjar</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A tipjar document for this agent, describing means for payment and reward.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:topic_interest" href="prop-73-foaftopic_interest.md">foaf:topic_interest</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A thing of interest to this person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:weblog" href="prop-74-foafweblog.md">foaf:weblog</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A weblog of some thing (whether person, group, company etc.).&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:yahooChatID" href="prop-77-foafyahoochatid.md">foaf:yahooChatID</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A Yahoo chat ID&quot;</span>
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