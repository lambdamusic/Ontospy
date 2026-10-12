# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#

from .. import * # import main ontospy VERSION 
from ..core.utils import *  
from .actions import ONTODOCS_VIZ_STATIC
from .utils import *
from .jinja_env import get_default_env

import zipfile
import os
import shutil

from pygments import highlight
from pygments.lexers.rdf import TurtleLexer
from pygments.formatters import HtmlFormatter

try:
    from .CONFIG import VISUALIZATIONS_LIST
    VISUALIZATIONS_LIST = VISUALIZATIONS_LIST['Visualizations']
except:  # Mother of all exceptions
    printDebug("Visualizations configuration file not found.", fg="red")
    raise


class VizFactory(object):
    """
    Object encapsulating common methods for building visualizations

    Tip: subclass and override as needed.
    """

    def __init__(self, ontospy_graph, title="", jinja2env = None):
        self.title = ''
        self.ontospy_graph = ontospy_graph
        self.static_files = []
        self.static_url = ""  # one used in templates
        self.final_url = None
        self.output_path = None
        self.output_path_static = None
        home = os.path.expanduser("~")
        self.output_path_DEFAULT = os.path.join(home, "ontospy-viz")
        self.template_name = ""
        self.main_file_name = ""
        self.static_root = ONTODOCS_VIZ_STATIC
        self.title = title or self.infer_best_title()
        self.basic_context_data = self._build_basic_context()
        self.jinja2env = jinja2env or get_default_env()
        self.written_files = set()  # absolute paths of the files written by the last build
        self.leftover_files = []  # files in the output folder that the last build didn't write

    def infer_best_title(self):
        """Selects something usable as a title for an ontospy graph. 
        If we have more than one ontology definition, use a generic title."""
        if self.ontospy_graph.all_ontologies:
            if len(self.ontospy_graph.all_ontologies) > 1:
                return f"RDF knowledge graph ({len(self.ontospy_graph.all_ontologies)} ontologies)"
            else:
                return self.ontospy_graph.all_ontologies[0].uri
        elif self.ontospy_graph.sources:
            if len(self.ontospy_graph.sources) > 1:
                return f"RDF knowledge graph {len(self.ontospy_graph.sources)} sources"
            else:
                return self.ontospy_graph.sources[0]
        else:
            return "Untitled"

    def build(self, output_path="", empty_folder=False):
        """method that should be inherited by all vis classes

        Files already in the output folder are kept (and overwritten if the build writes
        a file with the same name), unless `empty_folder` is True: then everything in the
        output folder is deleted first. Afterwards, files that the build didn't write are
        reported, as they may be left over from earlier builds.
        """

        self.written_files = set()
        self.output_path = self.checkOutputPath(output_path, empty_folder)
        self._buildStaticFiles()
        self.final_url = self._buildTemplates()
        self._warn_leftover_files()
        printDebug("Done.", "comment")
        printDebug("=> %s" % (self.final_url), "comment")
        return self.final_url

    def _buildTemplates(self):
        """
        do all the things necessary to build the viz
        should be adapted to work for single-file viz, or multi-files etc.

        :param output_path:
        :return:
        """
        #  in this case we only have one
        contents = self._renderTemplate(self.template_name, extraContext=None)
        # the main url used for opening viz
        f = self.main_file_name
        main_url = self._save2File(contents, f, self.output_path)
        return main_url

    def _renderTemplate(self, template_name, extraContext=None):
        """

        :param template_name: NOTE *relative* to templates folder
        :param extraContext: a dict that can be loaded on demand
        :return: the rendered template as a string
        """
        t = self.jinja2env.get_template(template_name)
        context = self.basic_context_data
        if extraContext and type(extraContext) == dict:
            context.update(extraContext)
        contents = safe_str(t.render(context))
        return contents

    def _buildStaticFiles(self):
        """ move over static files so that relative imports work
        Note: if a dir is passed, it is copied with all of its contents
        If the file is a zip, it is copied and extracted too
        # By default folder name is 'static', unless *output_path_static* is passed (now allowed only in special applications like KompleteVizMultiModel)
        """
        if not self.output_path_static:
            self.output_path_static = os.path.join(self.output_path, "static")
        # printDebug(self.output_path_static, "red")
        if not os.path.exists(self.output_path_static):
            os.makedirs(self.output_path_static)
        for x in self.static_files:
            source_f = os.path.join(self.static_root, x)
            dest_f = os.path.join(self.output_path_static, x)
            if os.path.isdir(source_f):
                # copy over any existing files, rather than deleting the folder first
                shutil.copytree(source_f, dest_f, dirs_exist_ok=True)
                for root, dirs, files in os.walk(dest_f):
                    for f in files:
                        self._record_written(os.path.join(root, f))
            else:
                shutil.copyfile(source_f, dest_f)
                self._record_written(dest_f)
                if x.endswith('.zip'):
                    printDebug("..unzipping")
                    zip_ref = zipfile.ZipFile(os.path.join(dest_f), 'r')
                    zip_ref.extractall(self.output_path_static)
                    for name in zip_ref.namelist():
                        self._record_written(os.path.join(self.output_path_static, name))
                    zip_ref.close()
                    printDebug("..cleaning up")
                    os.remove(dest_f)
                    # http://superuser.com/questions/104500/what-is-macosx-folder
                    shutil.rmtree(
                        os.path.join(self.output_path_static, "__MACOSX"))

    def preview(self):
        if self.final_url:
            import webbrowser
            webbrowser.open(self.final_url)
        else:
            printDebug("Nothing to preview")

    def _build_basic_context(self):
        """
        Return a standard dict used as a template context
        """
        # printDebug(str(self.ontospy_graph.toplayer_classes))
        topclasses = self.ontospy_graph.toplayer_classes[:]
        if len(topclasses) < 3:  # massage the toplayer!
            for topclass in self.ontospy_graph.toplayer_classes:
                for child in topclass.children():
                    if child not in topclasses: topclasses.append(child)

        if not self.static_url:
            self.static_url = "static/"  # default

        context_data = {
            "STATIC_URL": self.static_url,
            "gendocs_version": VERSION,
            "ontospy_graph": self.ontospy_graph,
            "topclasses": topclasses,
            "docs_title": self.title,
            "namespaces": self.ontospy_graph.namespaces,
            "stats": self.ontospy_graph.stats(),
            "sources": self.ontospy_graph.sources,
            "ontologies": self.ontospy_graph.all_ontologies,
            "classes": self.ontospy_graph.all_classes,
            "properties": self.ontospy_graph.all_properties,
            "objproperties": self.ontospy_graph.all_properties_object,
            "dataproperties": self.ontospy_graph.all_properties_datatype,
            "annotationproperties":
            self.ontospy_graph.all_properties_annotation,
            "skosConcepts": self.ontospy_graph.all_skos_concepts,
            "individuals": self.ontospy_graph.all_individuals,
        }

        return context_data

    def _save2File(self, contents, filename, path):
        filename = os.path.join(path, filename)
        f = open(filename, 'wb')
        f.write(contents)  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it
        self._record_written(filename)
        url = "file://" + filename
        return url

    def checkOutputPath(self, output_path, empty_folder=False):
        """
        Create the output path if needed. Files already there are kept, unless
        `empty_folder` is True: then the folder's contents are deleted (the folder itself
        is kept, eg in case it's a mounted volume).
        """
        if not output_path:
            # output_path = self.output_path_DEFAULT
            output_path = os.path.join(self.output_path_DEFAULT,
                                       slugify(unicode(self.title)))
        if os.path.exists(output_path):
            if empty_folder:
                self._empty_folder(output_path)
        else:
            os.makedirs(output_path)
        return output_path

    def _empty_folder(self, path):
        """Delete everything inside a folder, but not the folder itself"""
        printDebug("Emptying the output folder: %s" % path, dim=True)
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

    def _record_written(self, filename):
        self.written_files.add(os.path.abspath(filename))

    def _warn_leftover_files(self):
        """Report files in the output folder that this build didn't write: they may be
        left over from earlier builds, eg pages for entities no longer in the ontology.
        Hidden files (eg .DS_Store, .git) are ignored."""
        self.leftover_files = []
        for root, dirs, files in os.walk(self.output_path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                path = os.path.abspath(os.path.join(root, f))
                if not f.startswith(".") and path not in self.written_files:
                    self.leftover_files.append(path)
        if self.leftover_files:
            n = len(self.leftover_files)
            examples = ", ".join(os.path.relpath(x, self.output_path) for x in sorted(self.leftover_files)[:3])
            printDebug(
                "WARNING: %d file%s in the output folder %s not written by this build, eg %s. "
                "They may be left over from earlier builds: use the --emptyfolder option "
                "(or `empty_folder=True`) to delete everything in the folder first."
                % (n, "s" if n > 1 else "", "were" if n > 1 else "was", examples),
                fg="red")

    def highlight_code(self, ontospy_entity):
        """
        produce an html version of Turtle code with syntax highlighted
        using Pygments CSS
        """
        source = ontospy_entity.rdf_source()
        if not source:
            # no triples about the entity in the graph, eg an external superclass
            return {}
        try:
            pygments_code = highlight(source, TurtleLexer(), HtmlFormatter())
            pygments_code_css = HtmlFormatter().get_style_defs('.highlight')
            return {
                "pygments_code": pygments_code,
                "pygments_code_css": pygments_code_css
            }
        except Exception as e:
            printDebug("Error: Pygmentize Failed", "red")
            return {}
