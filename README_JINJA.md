# README - DJANGO TO JINJA MIGRATION


# TEMP - DONE
> single-html page 
> sigma
> markdown
> all D3 viz

Next:
> try multi page: how hard? is it worth it? 

python -m ontospy.gendocs.viz.viz_sigmajs

## NOW

Install extension https://pypi.org/project/jinja2-time/

{% now 'utc', '%a, %d %b %Y %H:%M:%S' %}



## IFCHANGED

DEPRECATED => See `watchchanges` in https://svn.python.org/projects/external/Jinja-1.1/docs/build/builtins.html

USING METHOD https://groups.google.com/g/pocoo-libs/c/uRsxf9ivv2c
AND ASSIGNMENTS https://jinja.palletsprojects.com/en/3.1.x/templates/#assignments


FOR ME: 

{% for each in o.annotations %}
{% ifchanged each.1 %}
    {% if not forloop.first %}</dl>{% endif %}
        <dt>{{each.1}}</dt>
{% endifchanged %}
        <dd>{{each.2|linebreaks}}</dd>
{% endfor %}

=======> 
BECOMES

{% for each in o.annotations() %}
{% if each.1 != variable_watcher  %}
    {% if not loop.first %}</dl>{% endif %}
        <dt>{{each.1}}</dt>
      {% set variable_watcher = each.1 %}
{% else %}
{% endif %}
<dd>{{each.2|linebreaks}}</dd>
{% endfor %}

OR 

{% for each in o.annotations %}
    {% if each.1 != variable_watcher  %}
        <dt>{{each.1}}</dt>
        {% set variable_watcher = each.1 %}
    {% else %}{% endif %}
<dd>{{each.2|linebreaks}}</dd>
{% endfor %}




## DEFAULT

See https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.default

{{s.qname|default:each.qname}}

=========> 
{{s.qname|default(each.qname)}}



## LINEBREAKS

Need to have your own impleementation
https://stackoverflow.com/questions/4901483/how-to-apply-django-jinja2-template-filters-escape-and-linebreaks-correctly

```
import re
from markupsafe import Markup, escape
from jinja2 import pass_eval_context

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@pass_eval_context
def linebreaks_filter(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                      for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

env.filters['linebreaks'] = linebreaks_filter
```




## METHOD CALLS

    {% for each in o.annotations %}
TypeError: 'method' object is not iterable

each.children() , each.parents() etc... each.rdf_source()|linebreaks

See 
https://stackoverflow.com/questions/59589889/difference-between-an-item-and-an-attribute-jinja-python



## IFEQUAL

ifequal becomes if X = Y


## WITH

{% with main_entity as each  %}
{% endwith %}

becomes 

{% set each = main_entity  %}


## COMMENTS

{% comment %}

becomes

{# 
comment
#}

See https://jinja.palletsprojects.com/en/3.1.x/templates/#comments