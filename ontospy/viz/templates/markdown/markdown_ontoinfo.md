{% extends "markdown_base.md" %}


{% block main_column %}


{% if ontology.annotations %}
### Metadata
{% for each in ontology.annotations %}
{% ifchanged each.1 %}
* {{each.1}}
{% endifchanged %}
    * {{each.2}}
{% endfor %}
{% endif %}


{% if ontology.annotations %}
### Metrics
{% for each in ontograph.stats %}
* {{each.0}}: **{{each.1}}**
{% endfor %}
{% endif %}


{% if ontology.namespaces %}
### Namespaces

Prefix   | URI      |
---------|----------|
{% for x,y in ontograph.namespaces %}**{{x}}**| [{{y}}]({{y}} "Open Url")|
 {% endfor %}
{% endif %}



{% endblock main_column %}

