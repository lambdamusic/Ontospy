# {{main_uri}}

Documentation automatically generated with [OntoSpy](http://ontospy.readthedocs.org/ "Open") on {% now "jS F Y H:i" %}

---	
	
{% block main_column %}




{% endblock main_column %}

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