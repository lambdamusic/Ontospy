{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "class"  %}
    
{% with main_entity as each  %}

## Class {{each.title}}


#### Tree
{% if each.parents %}
{% for s in each.parents %}
* [{{s.title}}]({{s.slug}}.md)
{% endfor %}
    * {{each.title}}
{% if each.children  %}
{% for s in each.children %}
        * [{{s.title}}]({{s.slug}}.md) 
{% endfor %}        
{% endif %}

{% else %}
* owl:Thing
    * {{each.title}}
{% if each.children  %}
{% for s in each.children %}
        * [{{s.title}}]({{s.slug}}.md) 
{% endfor %}        
{% endif %}

{% endif %}

{% if not each.children  %}
*NOTE* this is a leaf node.
{% endif %}

#### URI
{{each.uri}}

#### Description
{{each.bestDescription|linebreaks|default:"--"}}


{% if each.ancestors %}
#### Inherits from ({{ each.ancestors|length }})
{% for s in each.ancestors %}
- [{{s.title}}]({{s.slug}}.md)
{% endfor %}
{% else %}
#### Inherits from:
owl:Thing
{% endif %}


{% if each.instances %}
#### Has instances ({{ each.instances|length }})
{% for s in each.instances %}
- [{{s.title}}]({{s.slug}}.md)
{% endfor %}
{% endif %}


#### Implementation
```rdf
{{each.rdf_source|safe}}
```



{% if each.domain_of_inferred %}
#### Instances of {{each.title}} can have the following properties:

<table border="1" cellspacing="3" cellpadding="5" class="classproperties table-hover ">

    <tr>
        <th height="40">Property</th><th>Description</th><th>Expected Type</th>
    </tr>

    {% for group in each.domain_of_inferred  %}      

        {% for k,v in group.items  %}
            
        
        <tr style="background: lightcyan;text-align: left;">
            <th colspan="3" height="10" class="treeinfo"><span style="font-size: 80%;">
            From <a title="{{k.qname}}" href="{{k.slug}}.md" class="rdfclass">{{k.title}}</a></span>
            </th>
        </tr>       

            {% for prop in v  %}
            <tr>
                <td class="firsttd">
                    <a class="propcolor" title="{{prop.qname}}" href="{{prop.slug}}.md">{{prop.title}}</a>         
                </td>
                <td class="thirdtd">
                    <span>{{prop.bestDescription}}</span>
                </td>
                <td class="secondtd">
                    {% if  prop.ranges %}
                    {% for range in prop.ranges  %}

                        <a title="{{range.qname}}" href="{{range.slug}}.md" class="rdfclass">{{range.title}}</a>

                    {% endfor %}
                    {% else %}
                        <i>owl:Thing</i>
                    {% endif %}
                </td>
            </tr>

            {% endfor %}

        {% endfor %}

    {% endfor %}

</table>

{% endif %}



{% endwith %}
{% endifequal %}




{% endblock main_column %}