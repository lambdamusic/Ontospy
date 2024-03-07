
from jinja2 import Environment, PackageLoader, select_autoescape
import re
from markupsafe import Markup, escape
from jinja2 import pass_eval_context
from ontospy.core.utils import slugify

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

def slugify_filter(value):
    """A filter for legacy django templates to call that returns a slugified value."""
    return slugify(value)  # from ontospy.core.utils

@pass_eval_context
def linebreaks_filter(eval_ctx, value):
    """A filter for legacy django templates."""
    try:
        if not value:
            return ""
        result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                        for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result
    except:
        return value


def capfirst_filter(value):
    """A filter for legacy django templates to call that returns a capitalized value."""
    try:
        return value.capitalize()
    except:
        return value


def add_filter(value, integer_n):
    """A filter for legacy django templates."""
    try:
        return value + integer_n
    except:
        return value


def truncatewords_filter(data, l=20):
    """A filter for legacy django templates."""
    try:
        data_list = data.split()
        info = (" ".join(data_list[:l]) + '..') if len(data_list) > l else data
        return info
    except:
        return data


def d3_dendogram_height_filter(tot_objects):
    """A filter to generate dynamically the min height of a dendogram."""
    n = 50 * tot_objects
    if n < 800:
        return 800
    else:
        return n
    
def add_default_filters(env):
    env.filters['slugify'] = slugify_filter
    env.filters['linebreaks'] = linebreaks_filter
    env.filters['capfirst'] = capfirst_filter
    env.filters['add'] = add_filter
    env.filters['truncatewords'] = truncatewords_filter
    env.filters['d3_dendogram_height'] = d3_dendogram_height_filter

def get_default_env():
    # Setup Jinja2
    env = Environment(
        loader=PackageLoader('ontospy.gendocs.media', 'templates'),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=['jinja2_time.TimeExtension']
    )

    # Add custom filters
    add_default_filters(env)

    return env

# Create this global variable for backwards compatibility
env = get_default_env()
