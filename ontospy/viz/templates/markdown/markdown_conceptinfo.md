{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "concept"  %}
    
{% with main_entity as each  %}

# SKOS Concept {{each.qname}}


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
* skos:Concept
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
skos:Concept
{% endif %}


#### Implementation
```
{{each.serialize|safe}}
```

{% endwith %}
{% endifequal %}




{% endblock main_column %}