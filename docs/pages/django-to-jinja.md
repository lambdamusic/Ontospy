# Django to Jinja migration

As of version 2.0 (Oct 2022) Ontospy's visualization module replaces [Django](https://docs.djangoproject.com/en/4.1/ref/templates/builtins/) with [Jinja](https://jinja.palletsprojects.com/en/3.1.x/). 

This is to make Ontospy footprint more lightweight, as well as to simplify future maintenance of the library. Django offers a lot of functionalities that are not needed by the simple use case of Ontospy: cranking out HTML pages from templates.

This page contains information of Django specific template filters, or constructs, that are not directly usable with Jinja and how they have been updated. 

{% raw %}

## NOW

Django's template tag `now` can be used in Jinja after installing the extension https://pypi.org/project/jinja2-time/. 

Then you can do

```python
{% now 'utc', '%a, %d %b %Y %H:%M:%S' %}
```


## IFCHANGED

Django's template tag `ifchanged` does not exist in Jinja. So a custom logic for caching iteration values via [jinja assignments](https://jinja.palletsprojects.com/en/3.1.x/templates/#assignments) must be implemented. I found an example of this approach on https://groups.google.com/g/pocoo-libs/c/uRsxf9ivv2c

From 

```python
{% for each in o.annotations %}
    {% ifchanged each.1 %}
        {% if not forloop.first %}</dl>{% endif %}
            <dt>{{each.1}}</dt>
    {% endifchanged %}
    <dd>{{each.2|linebreaks}}</dd>
{% endfor %}
```

To

```python
{% for each in o.annotations() %}
    {% if each.1 != variable_watcher  %}
        {% if not loop.first %}</dl>{% endif %}
            <dt>{{each.1}}</dt>
        {% set variable_watcher = each.1 %}
    {% else %}
    {% endif %}
    <dd>{{each.2|linebreaks}}</dd>
{% endfor %}
```


## DEFAULT

Django's template tag `ifchanged` has a slightly diffent syntax in [Jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.default).

From

```python
{{s.qname|default:each.qname}}
```
To

```python
{{s.qname|default(each.qname)}}
```


## LINEBREAKS

Django's template filter `linebreaks` does not exist in Jinja. It can be implemented as a custom filter (see this [thread on SO](https://stackoverflow.com/questions/4901483/how-to-apply-django-jinja2-template-filters-escape-and-linebreaks-correctly))


```python
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

Django's templating language is 'relaxed' when it comes to resolving an object *attribute* or *method* call. In both cases, it's enough to pass the *attribute* or *method* name. 

With Jinja, *method* calls need to be followed by parentheses, like in Python.  See also https://stackoverflow.com/questions/59589889/difference-between-an-item-and-an-attribute-jinja-python


From 
```python
{% for each in o.annotations %}
```

To 
```python
{% for each in o.annotations() %}
```


PS this applies to `each.children()` , `each.parents()`, `each.rdf_source()` etc..



## IFEQUAL

From

```python
{% ifequal objtype "class" #}"""
```

To

```python
{% if objtype == "class" #}"""
```

## WITH

From 
```python
{% with main_entity as each  #}"""
...
{% endwith %}
```

To 

```python
{% set each = main_entity  #}"""
# no need to close anything
```

## COMMENTS

See https://jinja.palletsprojects.com/en/3.1.x/templates/#comments

From

```python
{% comment %}
```

To 

```python
{% 
comment
#}"""
```
{% endraw %}
