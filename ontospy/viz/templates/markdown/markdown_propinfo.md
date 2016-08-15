{% extends "markdown_base.md" %}
{% block main_column %}


{% ifequal main_entity_type "property"  %}
    
        {% with main_entity as each  %}


        <div class="entity-div">

            <h1 class="entity-section">Property: <a name="{{each.qname}}" href="{{each.slug}}.html">{{each.qname}}</a>
                <small>&nbsp;&nbsp;<a href="index.html" class="backlink">back to top</a></small>
            </h1>
            <hr>


            {% if not each.children  %}
            <p class="section-desc">
                <small>NOTE</small> this is a leaf node.</p>
            {% endif %}

            <p class="section-desc"><b>URI:</b>
                <br>
                {{each.uri}}
            </p>
 
            <p class="section-desc"><b>Description:</b>
                <br>
                {{each.bestDescription|default:"--"}}
            </p>

            {% if each.ancestors %}
                <p class="section-desc"><b>Inherits from <small>({{ each.ancestors|length }})</small>:</b>
                    <br />
                    {% for s in each.ancestors %}<a href="{{s.slug}}.html">{{s.qname}}</a> {% if not forloop.last %}|{% endif %} {% endfor %}
                </p>
            {% else %}

            {% endif %}



            {% if each.children %}
                <p class="section-desc"><b>Has sub-property <small>(direct)</small>:</b>
                    <br />
                    {% for s in each.children %}<a href="{{s.slug}}.html">{{s.qname}}</a> {% if not forloop.last %}|{% endif %} {% endfor %}
                </p>
            {% endif %}

            {% if 0 and each.descendants and each.descendants|length > each.children|length %}
                <p class="section-desc"><b>Has Sub Property <small>(all)   </small>:</b> {% for s in each.descendants %}<a href="{{s.slug}}.html">{{s.qname}}</a> {% if not forloop.last %}|{% endif %} {% endfor %}</p>
            {% endif %}



            <p class="section-desc"><b>Usage:</b>
                <br>
                {% if each.domains %}
                    {% for s in each.domains %}
                    <a href="{{s.slug}}.html">{{s.qname|default:s}}</a> {% if not forloop.last %} &amp;&amp; {% endif %} 
                    {% endfor %}
                {% else %}
                    owl:Thing
                {% endif %}
                =&gt;&nbsp;<span class="highlight_entity">{{each.qname}}</span>&nbsp;=&gt;&nbsp;
                {% if each.ranges %}
                    {% for s in each.ranges %}
                    <a href="{{s.slug}}.html">{{s.qname|default:s}}</a> {% if not forloop.last %} &amp;&amp; {% endif %} 
                    {% endfor %}
                {% else %}
                    owl:Thing
                {% endif %}
            

            </p>




            <small class="implementation_title">Implementation:</small>
            {% if pygments_code %}
                {{pygments_code|safe}}
            {% else %}
                 <div class="implementation">
                    <code>{{each.serialize|linebreaks}}</code>
                </div>               
            {% endif %}

        </div>

        {% endwith %}



{% endifequal %}




{% endblock main_column %}