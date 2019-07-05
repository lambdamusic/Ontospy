{% extends "markdown_base.md" %}


{% block main_column %}

# _Vocabulary: [{{docs_title}}](index.md)_

---

{% if ontologies %}
#### Metadata
{% for ontology in ontologies %}
**{{ontology.uri}}**
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
{% endfor %}
{% endif %}


#### Metrics
{% for each in stats %}
* {{each.0}}: **{{each.1}}**
{% endfor %}



{% if namespaces %}
#### Namespaces

Prefix   | URI      |
---------|----------|
{% for x,y in namespaces %}**{{x}}**| [{{y}}]({{y}} "Open Url")|
 {% endfor %}
{% endif %}


---


## Entities  

{% if ontospy_graph.all_classes%}
#### Classes ({{ontospy_graph.all_classes|length}})

{% for each in ontospy_graph.all_classes %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_skos_concepts %}
#### SKOS Concepts ({{ontospy_graph.all_skos_concepts|length}})

{% for each in ontograph.all_skos_concepts  %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_object %}
#### Object Properties ({{ontospy_graph.all_properties_object|length}})

{% for each in ontospy_graph.all_properties_object %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_datatype %}
#### Datatype Properties ({{ontospy_graph.all_properties_datatype|length}})

{% for each in ontospy_graph.all_properties_datatype %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_annotation %}
#### Annotation Properties ({{ontograph.all_properties_annotation|length}})

{% for each in ontospy_graph.all_properties_annotation  %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if not ontospy_graph.all_properties_object and not ontospy_graph.all_properties_datatype and not ontospy_graph.all_properties_annotation %}
{% if ontospy_graph.all_properties %}
#### Properties ({{ontospy_graph.all_properties|length}})

{% for each in ontospy_graph.all_properties  %}
- [{{each.qname}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}
{% endif %}



{% endblock main_column %}
