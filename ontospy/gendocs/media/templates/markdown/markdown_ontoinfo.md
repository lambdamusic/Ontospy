{% extends "markdown/markdown_base.md" %}


{% block main_column %}

# _Vocabulary: [{{docs_title}}](index.md)_

---

{% if ontologies %}
#### Metadata
{% for ontology in ontologies %}
**{{ontology.uri}}**
{% if ontology.metadata() %}
{#- each property once, sorted; blank nodes (eg an editor) nested under a bullet with their name (#23) -#}
{% macro md_metadata(items, indent) %}{% for prop, values in items %}
{{indent}}* {{prop}}{% for v in values %}{% if v is mapping %}
{{indent}}    * {{ v.label or "_(blank node)_" }}{{ md_metadata(v.properties, indent ~ "        ") }}{% else %}
{{indent}}    * {% if v is url %}[{{v}}]({{v}}){% else %}{{ v|replace("\r\n", " ")|replace("\n", " ") }}{% endif %}{% endif %}{% endfor %}{% endfor %}{% endmacro %}
{{ md_metadata(ontology.metadata(), "") }}
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

{% if ontospy_graph.all_classes %}
#### Classes ({{ontospy_graph.all_classes|length}})

{% for each in ontospy_graph.all_classes %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_skos_concepts %}
#### SKOS Concepts ({{ontospy_graph.all_skos_concepts|length}})

{% for each in ontospy_graph.all_skos_concepts  %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_object %}
#### Object Properties ({{ontospy_graph.all_properties_object|length}})

{% for each in ontospy_graph.all_properties_object %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_datatype %}
#### Datatype Properties ({{ontospy_graph.all_properties_datatype|length}})

{% for each in ontospy_graph.all_properties_datatype %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if ontospy_graph.all_properties_annotation %}
#### Annotation Properties ({{ontospy_graph.all_properties_annotation|length}})

{% for each in ontospy_graph.all_properties_annotation  %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% if not ontospy_graph.all_properties_object and not ontospy_graph.all_properties_datatype and not ontospy_graph.all_properties_annotation %}
{% if ontospy_graph.all_properties %}
#### Properties ({{ontospy_graph.all_properties|length}})

{% for each in ontospy_graph.all_properties  %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}
{% endif %}


{% if ontospy_graph.all_individuals %}
#### Individuals ({{ontospy_graph.all_individuals|length}})

{% for each in ontospy_graph.all_individuals  %}
- [{{each.title}}]({{each.slug}}.md "Open")
{% endfor %}

{% endif %}


{% endblock main_column %}
