{# Macros for SHACL constraints in markdown, see ontospy/core/shacl_helper.py (backlog #37).
   The markdown counterpart of html-multi/browser/shacl_macros.html. A table row must stay
   on one line, so cell contents go through cell(), and values are separated by <br>. #}


{# text for a table cell: on one line, with | escaped #}
{% macro cell(text) -%}
  {{ text|string|replace("\r\n", " ")|replace("\n", " ")|replace("|", "\\|") }}
{%- endmacro %}


{# a Term: linked to its page if the graph defines it, else in italics #}
{% macro term(t) -%}
  {%- if t.entity -%}[{{ cell(t.qname) }}]({{t.entity.slug}}.md){%- else -%}*{{ cell(t.qname) }}*{%- endif -%}
{%- endmacro %}


{# a value of a constraint: a Term, or text #}
{% macro value(v) -%}
  {%- if v.qname is defined -%}{{ term(v) }}{%- else -%}`{{ cell(v) }}`{%- endif -%}
{%- endmacro %}


{# a list of (name, [values]), eg the constraints other than cardinality and type #}
{% macro constraint_list(items, sep="<br>") -%}
  {%- for name, values in items -%}
    **{{name}}** {% if name in ["sh:or", "sh:xone", "sh:and"] -%}
      {%- set op = {"sh:or": " \\| ", "sh:xone": " xor ", "sh:and": " & "}[name] -%}
      ( {% for v in values %}`{{ cell(v) }}`{% if not loop.last %}{{op}}{% endif %}{% endfor %} )
    {%- else -%}
      {% for v in values %}{{ value(v) }}{% if not loop.last %}, {% endif %}{% endfor %}
    {%- endif -%}
    {%- if not loop.last %}{{sep}}{% endif -%}
  {%- endfor -%}
{%- endmacro %}


{# the PROPERTY cell: the property, linked if defined in the ontology, or the path #}
{% macro path(constraint) -%}
  {%- set prop = constraint.property_obj.onto_property -%}
  {%- if prop -%}[{{prop.qname}}]({{prop.slug}}.md){%- else -%}`{{ cell(constraint.property_obj.qname) }}`{%- endif -%}
{%- endmacro %}


{# the DESCRIPTION cell: the shape's sh:name and sh:description, else the property's comment #}
{% macro description(constraint) -%}
  {%- if constraint.sh_name %}**{{ cell(constraint.sh_name|sort|join(", ")) }}**<br>{% endif -%}
  {%- if constraint.sh_description -%}
    {%- for x in constraint.sh_description|sort %}{{ cell(x) }}{% if not loop.last %}<br>{% endif %}{% endfor -%}
  {%- elif constraint.rdfs_comment -%}
    {%- for x in constraint.rdfs_comment|sort %}{{ cell(x) }}{% if not loop.last %}<br>{% endif %}{% endfor -%}
  {%- endif -%}
  {%- if constraint.sh_message %}<br>*sh:message* {{ cell(constraint.sh_message|sort|join("; ")) }}{% endif -%}
{%- endmacro %}


{# a table of constraints, with a header row for each class (in a class's list) #}
{% macro constraints_table(constraints, with_property_info=False) -%}
{%- set columns = 8 if with_property_info else 6 -%}
| Property |{% if with_property_info %} Property type |{% endif %} Description | Min | Max | Value type | Other constraints |{% if with_property_info %} Global range |{% endif %}
|{% for i in range(columns) %}---|{% endfor %}
{% for constraint in constraints -%}
{%- if constraint.header -%}
| **{{constraint.header}}** |{% for i in range(columns - 1) %} |{% endfor %}
{% else -%}
| {{ path(constraint) }} |
{%- if with_property_info %} {% for x in constraint.rdftype_qname|sort %}{{x}}{% if not loop.last %}<br>{% endif %}{% else %}--{% endfor %} |{% endif -%}
{{" "}}{{ description(constraint) }} | {{constraint.sh_minCount|sort|join(", ")|default("0", true)}} | {{constraint.sh_maxCount|sort|join(", ")|default("*", true)}} | {% for t in constraint.value_types %}{{ term(t) }}{% if not loop.last %}<br>{% endif %}{% endfor %} | {{ constraint_list(constraint.other_constraints) }} |
{%- if with_property_info %} {% for t in constraint.rdfs_range|sort(attribute="qname") %}{{ term(t) }}{% if not loop.last %}<br>{% endif %}{% else %}*--*{% endfor %} |{% endif %}
{% endif -%}
{%- endfor -%}
{%- endmacro %}
