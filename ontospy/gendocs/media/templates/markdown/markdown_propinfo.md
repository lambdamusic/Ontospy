{% extends "markdown/markdown_base.md" %}
{% block main_column %}


{% if main_entity_type == "property"  %}

{% set each = main_entity  %}

## Property {{each.title}}


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
* rdf:Property
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
{{each.bestDescription()|default("--")}}

{% if each.seeAlso() %}
#### See also
{% for x in each.seeAlso() %}
* {% if x is url %}[{{x}}]({{x}}){% else %}{{x}}{% endif %}
{% endfor %}
{% endif %}

{% if each.ancestors() %}
#### Inherits from ({{ each.ancestors()|length }})
{% for s in each.ancestors() %}
- [{{s.title}}]({{s.slug}}.md)
{% endfor %}
{% else %}
#### Inherits from:
owl:Thing
{% endif %}


#### Usage
{% set domains = each.domains or each.domains_inferred %}{% set ranges = each.ranges or each.ranges_inferred %}
{% if domains %}
{% for s in domains %}
[{{s.title}}]({{s.slug}}.md){% if not loop.last %} &amp;&amp; {% endif %}
{% endfor %}{% if not each.domains %} _(inferred)_{% endif %}{% else %}owl:Thing{% endif %}=&gt;&nbsp;_{{each.title}}_&nbsp;=&gt;&nbsp;{% if ranges %}{% for s in ranges %}[{{s.title}}]({{s.slug}}.md){% if not loop.last %} &amp;&amp; {% endif %}{% endfor %}{% if not each.ranges %} _(inferred)_{% endif %}{% else %}owl:Thing{% endif %}

{% if not each.domains and domains or not each.ranges and ranges %}_(inferred) = inherited from superproperties_{% endif %}

#### Implementation
```rdf
{{each.rdf_source()|safe}}
```


{% endif %}




{% endblock main_column %}
