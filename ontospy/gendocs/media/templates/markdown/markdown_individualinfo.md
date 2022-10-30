{% extends "markdown/markdown_base.md" %}
{% block main_column %}


{% if main_entity_type == "individual"  %}
    
{% set each =  main_entity  %}

# Individual {{each.title}}


#### URI
{{each.uri}}

#### Description
{{each.bestDescription()|linebreaks|default("--")}}


{% if each.instance_of %}
#### Is instance of ({{ each.instance_of|length }})
{% for s in each.instance_of %}
- [{{s.title}}]({{s.slug}}.md)
{% endfor %}
{% else %}
#### Is instance of:
owl:Thing
{% endif %}


#### Implementation
```rdf
{{each.rdf_source()|safe}}
```

{% endif %}




{% endblock main_column %}