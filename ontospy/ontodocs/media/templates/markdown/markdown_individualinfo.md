{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "individual"  %}
    
{% with main_entity as each  %}

# Individual {{each.title}}


#### URI
{{each.uri}}

#### Description
{{each.bestDescription|linebreaks|default:"--"}}


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
{{each.rdf_source|safe}}
```

{% endwith %}
{% endifequal %}




{% endblock main_column %}