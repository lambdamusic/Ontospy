# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


from . import *  # imports __init__
from .. import *
from ..core.entities import OntoClass, OntoProperty, OntoSKOSConcept, Ontology


# TEMPLATE: MARKDOWN EXPORT - MULTI FILE


#
# ===========
# Comments:
# ===========
#





def run(graph, save_on_github=False, main_entity=None):
    """
    From a graph instance outputs a nicely formatted html documentation file.
    
    2016-08-07: hacked for multi file save
    """

    try:
        ontology = graph.ontologies[0]
        uri = ontology.uri
    except:
        ontology = None
        uri = ";".join([s for s in graph.sources])
        
    context = {
                    "ontology": ontology,
                    "main_uri" : uri,
                    "ontospy_version" : VERSION,
                    "ontograph": graph,
                    "STATIC_PATH": ONTOSPY_VIZ_STATIC,
                }
    

    # Pygments CSS
    # try:
    #     from pygments import highlight
    #     from pygments.lexers.rdf import TurtleLexer
    #     from pygments.formatters import HtmlFormatter
    # 
    #     pygments_code = highlight(main_entity.serialize(), TurtleLexer(), HtmlFormatter())
    #     pygments_code_css = HtmlFormatter().get_style_defs('.highlight')
    #     context.update({ "pygments_code" : pygments_code,
    #                      "pygments_code_css": pygments_code_css
    #                      })
    # except Exception, e:
    #     pass
    # 

        
    if type(main_entity) == OntoClass:
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "markdown/markdown_classinfo.md", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "class"
                         })
    elif type(main_entity) == OntoProperty:
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "markdown/markdown_propinfo.md", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "property"
                         })
    elif type(main_entity) == OntoSKOSConcept:
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "markdown/markdown_conceptinfo.md", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "concept"
                         })
    else:
            # if type(main_entity) == Ontology:
        ontotemplate = open(ONTOSPY_VIZ_TEMPLATES + "markdown/markdown_ontoinfo.md", "r")


    t = Template(ontotemplate.read())
    c = Context(context)

    rnd = t.render(c)

    return safe_str(rnd)







if __name__ == '__main__':
    """
    > python -m viz.viz_markdown

    2016-08-04: # testing bypassing the usual abstract routine so to generate multiple files

    """
    import os, sys
    try:

        # script for testing - must launch this module direclty eg

        func = locals()["run"] # main func dynamically
        # run_test_viz(func)

        import webbrowser, random

        ontouri = get_localontologies()[random.randint(0, 10)] # [13]=foaf #
        print("Testing with URI: %s" % ontouri)

        g = get_pickled_ontology(ontouri)
        if not g:
            g = do_pickle_ontology(ontouri)


        def _saveVizLocally(contents, filename="index.md", path=None):
            if not path:
                filename = ONTOSPY_LOCAL_VIZ + "/" + filename
            else:
                filename = os.path.join(path, filename)

            f = open(filename, 'wb')
            f.write(contents)  # python will convert \n to os.linesep
            f.close()  # you can omit in most cases as the destructor will call it

            url = "file://" + filename
            return url

        from os.path import expanduser
        home = expanduser("~")
        DEST_FOLDER = os.path.join(home, "ontospy-viz/markdown")
        if not os.path.exists(DEST_FOLDER):
            os.makedirs(DEST_FOLDER)

        # main index page for graph
        contents = func(g, False, None)
        index_url = _saveVizLocally(contents, "index.md", DEST_FOLDER)
        
        entities = [g.classes, g.properties, g.skosConcepts]
        for group in entities:
            for c in group:
                # getting main func dynamically
                contents = func(g, False, c)
                _filename = c.slug + ".md"
                url = _saveVizLocally(contents, _filename, DEST_FOLDER)

        if index_url:  # open browser
            import webbrowser
            webbrowser.open(index_url)



        sys.exit(0)

    except KeyboardInterrupt as e: # Ctrl-C
        raise e



