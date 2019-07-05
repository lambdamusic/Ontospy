{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "property"  %}

{% with main_entity as each  %}

## Property {{each.qname}}


#### Tree
{% if each.parents %}
{% for s in each.parents %}
* [{{s.qname}}]({{s.slug}}.md)
{% endfor %}
    * {{each.qname}}
{% if each.children  %}
{% for s in each.children %}
        * [{{s.qname}}]({{s.slug}}.md)
{% endfor %}        
{% endif %}

{% else %}
* rdf:Property
    * {{each.qname}}
{% if each.children  %}
{% for s in each.children %}
        * [{{s.qname}}]({{s.slug}}.md)
{% endfor %}        
{% endif %}

{% endif %}

{% if not each.children  %}
*NOTE* this is a leaf node.
{% endif %}

#### URI
{{each.uri}}

#### Description
{{each.bestDescription|default:"--"}}

{% if each.ancestors %}
#### Inherits from ({{ each.ancestors|length }})
{% for s in each.ancestors %}
- [{{s.qname}}]({{s.slug}}.md)
{% endfor %}
{% else %}
#### Inherits from:
owl:Thing
{% endif %}


#### Usage
{% if each.domains %}
{% for s in each.domains %}
[{{s.qname}}]({{s.slug}}.md){% if not forloop.last %} &amp;&amp; {% endif %}
{% endfor %}{% else %}owl:Thing{% endif %}=&gt;&nbsp;_{{each.qname}}_&nbsp;=&gt;&nbsp;{% if each.ranges %}{% for s in each.ranges %}[{{s.qname}}]({{s.slug}}.md){% if not forloop.last %} &amp;&amp; {% endif %}{% endfor %}{% else %}owl:Thing{% endif %}

#### Implementation
```
{{each.rdf_source|safe}}
```


{% endwith %}
{% endifequal %}




{% endblock main_column %}
