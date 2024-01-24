{% extends "markdown/markdown_base.md" %}
{% block main_column %}


{% if main_entity_type == "class"  %}
    
{% set each = main_entity   %}

## Class {{each.title}}


#### Tree
{% if each.parents() %}
{% for s in each.parents() %}
* [{{s.title}}]({{s.slug}}.md)
{% endfor %}
    * {{each.title}}
{% if each.children()  %}
{% for s in each.children() %}
        * [{{s.title}}]({{s.slug}}.md) 
{% endfor %}        
{% endif %}

{% else %}
* owl:Thing
    * {{each.title}}
{% if each.children()  %}
{% for s in each.children() %}
        * [{{s.title}}]({{s.slug}}.md) 
{% endfor %}        
{% endif %}

{% endif %}

{% if not each.children()  %}
*NOTE* this is a leaf node.
{% endif %}

#### URI
{{each.uri}}

#### Description
{{each.bestDescription()|linebreaks|default("--")}}


{% if each.ancestors() %}
#### Inherits from ({{ each.ancestors()|length }})
{% for s in each.ancestors() %}
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
{{each.rdf_source()|safe}}
```



{% if each.domain_of_inferred %}
#### Instances of {{each.title}} can have the following properties:

{% for group in each.domain_of_inferred  %}      
    {%- for k,v in group.items()  -%}
          
##### From [{{k.title}}]({{k.slug}}.md):

| Property | Description | Expected Type |
|----------|-------------|---------------|
{% for prop in v -%}
| [{{prop.title}}]({{prop.slug}}.md) | {{prop.bestDescription()}} | 
            {%- if  prop.ranges -%}
                {%- for range in prop.ranges -%} 
[{{range.title}}]({{range.slug}}.md)
                {%- endfor -%}
            {%- else -%} 
*owl:Thing*
            {%- endif -%} 
|
{% endfor %}
{% endfor %}
{% endfor %}

{% endif %}


{% endif %}

{% endblock main_column %}
