{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "property"  %}

{% with main_entity as each  %}

## Property {{each.title}}


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
* rdf:Property
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


#### Usage
{% if each.domains %}
{% for s in each.domains %}
[{{s.title}}]({{s.slug}}.md){% if not forloop.last %} &amp;&amp; {% endif %}
{% endfor %}{% else %}owl:Thing{% endif %}=&gt;&nbsp;_{{each.title}}_&nbsp;=&gt;&nbsp;{% if each.ranges %}{% for s in each.ranges %}[{{s.title}}]({{s.slug}}.md){% if not forloop.last %} &amp;&amp; {% endif %}{% endfor %}{% else %}owl:Thing{% endif %}

#### Implementation
```rdf
{{each.rdf_source|safe}}
```


{% endwith %}
{% endifequal %}




{% endblock main_column %}
