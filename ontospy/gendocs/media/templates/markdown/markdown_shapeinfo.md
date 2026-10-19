{% extends "markdown/markdown_base.md" %}
{% import "markdown/shacl_macros.md" as shacl %}
{% block main_column %}

{% set each = main_entity %}

## Shape {{each.title}}

#### URI
{{each.uri}}

{% if each.bestDescription() %}
#### Description
{{each.bestDescription()}}
{% endif %}

{% if each.targets %}
#### Targets ({{each.targets|length}})
{% for kind, t in each.targets %}
* {{ shacl.term(t) }} _{{kind}}_
{% endfor %}
{% endif %}

{% if each.used_by %}
#### Used by ({{each.used_by|length}})
{% for t in each.used_by %}
* {{ shacl.term(t) }}
{% endfor %}
{% endif %}

{% if each.node_constraints %}
#### Node constraints
{% for item in each.node_constraints %}
* {{ shacl.constraint_list([item]) }}
{% endfor %}
{% endif %}

{% if each.shacl_constraints %}
#### Property constraints ({{each.shacl_constraints|length}})

{{ shacl.constraints_table(each.shacl_constraints) }}
{% endif %}

#### Implementation
```rdf
{{each.rdf_source()|safe}}
```

{% endblock main_column %}
