{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "concept"  %}
    
{% with main_entity as each  %}

# SKOS Concept {{each.title}}


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
* skos:Concept
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
skos:Concept
{% endif %}


#### Implementation
```rdf
{{each.rdf_source|safe}}
```

{% endwith %}
{% endifequal %}




{% endblock main_column %}