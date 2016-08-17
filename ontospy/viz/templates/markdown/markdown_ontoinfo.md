{% extends "markdown_base.md" %}


{% block main_column %}

# {{main_uri}}

---

### Metadata
{% if ontology.annotations %}
{% for each in ontology.annotations %}
{% ifchanged each.1 %}
* {{each.1}}
{% endifchanged %}
    * {{each.2}}
{% endfor %}
{% else %}
_No ontology metadata available_
{% endif %}


### Metrics
{% for each in ontograph.stats %}
* {{each.0}}: **{{each.1}}**
{% endfor %}



{% if ontology.namespaces %}
### Namespaces

Prefix   | URI      |
---------|----------|
{% for x,y in ontograph.namespaces %}**{{x}}**| [{{y}}]({{y}} "Open Url")|
 {% endfor %}
{% endif %}


---


## Index 

{% if ontograph.classes %}
### Classes ({{ontograph.classes|length}}) 

{% for each in ontograph.classes  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	


{% if ontograph.skosConcepts %}
### SKOS Concepts ({{ontograph.skosConcepts|length}}) 

{% for each in ontograph.skosConcepts  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	


{% if ontograph.objectProperties %}
### Object Properties ({{ontograph.objectProperties|length}}) 

{% for each in ontograph.objectProperties  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	


{% if ontograph.datatypeProperties %}
### Datatype Properties ({{ontograph.datatypeProperties|length}}) 

{% for each in ontograph.datatypeProperties  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	


{% if ontograph.annotationProperties %}
### Annotation Properties ({{ontograph.annotationProperties|length}}) 

{% for each in ontograph.annotationProperties  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	


{% if not ontograph.objectProperties and not ontograph.dataProperties and not ontograph.annotationProperties %}
{% if ontograph.properties %}
### Properties ({{ontograph.properties|length}}) 

{% for each in ontograph.properties  %}
- [{{each.qname}}]({{each.slug}}.md "Open") 
{% endfor %}

{% endif %}	
{% endif %}	



{% endblock main_column %}

