
from jinja2 import Environment, PackageLoader, select_autoescape
import re
from markupsafe import Markup, escape
from jinja2 import pass_eval_context
from ontospy.core.utils import slugify

#
# SET UP JINJA2
#
env = Environment(
    loader=PackageLoader('ontospy.gendocs.media', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    extensions=['jinja2_time.TimeExtension']
)


#############################
####### JINJA2 CUSTOM FILTERS
###


#
# FILTER
#

def slugify_filter(value):
    """A filter for legacy django templates to call that returns a slugified value."""
    return slugify(value)  # from ontospy.core.utils

env.filters['slugify'] = slugify_filter


#
# FILTER
#

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@pass_eval_context
def linebreaks_filter(eval_ctx, value):
    """A filter for legacy django templates."""
    if not value:
        return ""
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                      for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result

env.filters['linebreaks'] = linebreaks_filter

#
# FILTER
#


def capfirst_filter(value):
    """A filter for legacy django templates to call that returns a capitalized value."""
    try:
        return value.capitalize()
    except:
        return value

env.filters['capfirst'] = capfirst_filter



#
# FILTER
#


def add_filter(value, integer_n):
    """A filter for legacy django templates."""
    try:
        return value + integer_n
    except:
        return value

env.filters['add'] = add_filter



#
# FILTER
#


def truncatewords_filter(data, l=20):
    """A filter for legacy django templates."""
    try:
        data_list = data.split()
        info = (" ".join(data_list[:l]) + '..') if len(data_list) > l else data
        return info
    except:
        return data


env.filters['truncatewords'] = truncatewords_filter

