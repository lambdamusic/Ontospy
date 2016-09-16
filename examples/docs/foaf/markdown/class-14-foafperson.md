Vocabulary: [http://xmlns.com/foaf/0.1/](index.md) 



---	
	




    


## Class foaf:Person


### Tree


* [http://www.w3.org/2000/10/swap/pim/contact#Person](class-2-httpwwww3org200010swappimcontactperson.md)

* [http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing](class-3-httpwwww3org200301geowgs84_posspatialthing.md)

* [foaf:Agent](class-4-foafagent.md)

    * foaf:Person





*NOTE* this is a leaf node.


### URI
http://xmlns.com/foaf/0.1/Person

### Description
&quot;A person.&quot;



### Inherits from (3)

- [http://www.w3.org/2000/10/swap/pim/contact#Person](class-2-httpwwww3org200010swappimcontactperson.md)

- [http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing](class-3-httpwwww3org200301geowgs84_posspatialthing.md)

- [foaf:Agent](class-4-foafagent.md)





### Implementation
```
<p>@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .<br />@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .<br />@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .<br />@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .<br />@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .<br />@prefix skos: &lt;http://www.w3.org/2004/02/skos/core#&gt; .<br />@prefix vs: &lt;http://www.w3.org/2003/06/sw-vocab-status/ns#&gt; .<br />@prefix wot: &lt;http://xmlns.com/wot/0.1/&gt; .<br />@prefix xml: &lt;http://www.w3.org/XML/1998/namespace&gt; .<br />@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .</p>

<p>foaf:Person a rdfs:Class,<br />        owl:Class ;<br />    rdfs:label &quot;Person&quot; ;<br />    rdfs:comment &quot;A person.&quot; ;<br />    rdfs:isDefinedBy foaf: ;<br />    rdfs:subClassOf &lt;http://www.w3.org/2000/10/swap/pim/contact#Person&gt;,<br />        &lt;http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing&gt;,<br />        foaf:Agent ;<br />    owl:disjointWith foaf:Organization,<br />        foaf:Project ;<br />    vs:term_status &quot;stable&quot; .</p>

<p></p>
```




### Instances of foaf:Person can have the following properties:

<table border="1" cellspacing="3" cellpadding="5" class="classproperties table-hover ">

    <tr>
        <th height="40">Property</th><th>Description</th><th>Expected Type</th>
    </tr>

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="foaf:Person" href="class-14-foafperson.md" class="rdfclass">foaf:Person</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:currentProject" href="prop-24-foafcurrentproject.md">foaf:currentProject</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A current project this person works on.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:familyName" href="prop-28-foaffamilyname.md">foaf:familyName</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The family name of some person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:family_name" href="prop-29-foaffamily_name.md">foaf:family_name</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The family name of some person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:firstName" href="prop-30-foaffirstname.md">foaf:firstName</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The first name of a person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:geekcode" href="prop-33-foafgeekcode.md">foaf:geekcode</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A textual geekcode for this person, see http://www.geekcode.com/geek.html&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:img" href="prop-39-foafimg.md">foaf:img</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;An image that can be used to represent some thing (ie. those depictions which are particularly representative of something, eg. one&#39;s photo on a homepage).&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Image" href="class-7-foafimage.md" class="rdfclass">foaf:Image</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:knows" href="prop-43-foafknows.md">foaf:knows</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A person known by this person (indicating some level of reciprocated interaction between the parties).&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Person" href="class-14-foafperson.md" class="rdfclass">foaf:Person</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:lastName" href="prop-44-foaflastname.md">foaf:lastName</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The last name of a person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:myersBriggs" href="prop-53-foafmyersbriggs.md">foaf:myersBriggs</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A Myers Briggs (MBTI) personality classification.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:pastProject" href="prop-58-foafpastproject.md">foaf:pastProject</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A project this person has previously worked on.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:plan" href="prop-60-foafplan.md">foaf:plan</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A .plan comment, in the tradition of finger and &#39;.plan&#39; files.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:publications" href="prop-62-foafpublications.md">foaf:publications</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A link to the publications of this person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:schoolHomepage" href="prop-63-foafschoolhomepage.md">foaf:schoolHomepage</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A homepage of a school attended by the person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:surname" href="prop-67-foafsurname.md">foaf:surname</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;The surname of some person.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="" href=".md" class="rdfclass"></a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:workInfoHomepage" href="prop-75-foafworkinfohomepage.md">foaf:workInfoHomepage</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A work info homepage of some person; a page about their work for some organization.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:workplaceHomepage" href="prop-76-foafworkplacehomepage.md">foaf:workplaceHomepage</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A workplace homepage of some person; the homepage of an organization they work for.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="foaf:Document" href="class-5-foafdocument.md" class="rdfclass">foaf:Document</a>

                    
                    
                </td>
            </tr>

            

        

          

        
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing" href="class-3-httpwwww3org200301geowgs84_posspatialthing.md" class="rdfclass">http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing</a></span>
            </th>
        </tr>       

            
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="foaf:based_near" href="prop-22-foafbased_near.md">foaf:based_near</a>         
                </td>
                <td class="thirdtd">
                    <span>&quot;A location that something is based near, for some broadly human notion of near.&quot;</span>
                </td>
                <td class="secondtd">
                    
                    

                        <a title="http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing" href="class-3-httpwwww3org200301geowgs84_posspatialthing.md" class="rdfclass">http://www.w3.org/2003/01/geo/wgs84_pos#SpatialThing</a>

                    
                    
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