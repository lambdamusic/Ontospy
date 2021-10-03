# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
"""
Ontospy Shell Module
michele.pasin@gmail.com

# docs:
# https://docs.python.org/2/library/cmd.html
# https://hg.python.org/cpython/file/2.7/Lib/cmd.py
# http://pymotw.com/2/cmd/


"""


import sys
import os
import cmd
import random
import shutil
import platform
try:
    import urllib2
except:
    import urllib as urllib2
# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

from pyfiglet import Figlet
from colorama import Fore, Style

from subprocess import PIPE, Popen
PY2 = sys.version < '3'
WINDOWS = os.name == 'nt'
EOL = '\r\n' if WINDOWS and not PY2 else '\n'


from .. import *  # load top level __init__
from ..VERSION import VERSION

from ..core import ONTOSPY_LOCAL
from ..core import manager
from ..core import actions
from ..core.ontospy import Ontospy
from ..core.utils import *


from .shell_quotes import *  # quotes


f = Figlet(font='slant')
_intro_ = """***
The Command Line Ontology Browser (%s)
***											  """

STARTUP_MESSAGE = f.renderText('Ontospy') + Style.BRIGHT + _intro_ % VERSION + Style.RESET_ALL


def _get_prompt(onto="", entity=""):
    """
    Global util that changes the prompt contextually
    :return: [Ontospy]>(cidoc_crm_v5.0...)>(class:E1.CRM_Entity)>
    """
    base_text, onto_text, entity_text = "", "", ""
    base_color, onto_color, entity_color = Fore.RED + Style.BRIGHT, Fore.BLACK + Style.DIM, Fore.BLACK

    if not onto and not entity:
        base_text = base_color + '[Ontospy]' + Style.RESET_ALL

    if onto and not entity:
        _tmp = onto_color + '(%s)' % onto
        onto_text = _tmp + Style.RESET_ALL

    if entity:
        _tmp = onto_color + Style.BRIGHT + '(%s)' % truncate(onto, 15)
        onto_text = _tmp + Style.RESET_ALL

        _tmp2 = entity_color + '(%s:%s)' % (entity['type'], entity['name'])
        entity_text = "-" + _tmp2 + Style.RESET_ALL

    return base_text + onto_text + entity_text + "> "


class Shell(cmd.Cmd):
    """Simple command processor example."""

    prompt = _get_prompt()
    intro = "Type 'help' to get started, TAB to explore commands.\n"

    doc_header = 'Commands available (type `help <command>` to get help):'
    misc_header = 'Miscellaneous'
    undoc_header = 'Undocumented commands'

    ruler = '-'
    maxcol = 80

    INFO_OPTS = ['namespaces', 'toplayer', 'parents',
                 'children', 'ancestors', 'descendants', 'inferred_usage']
    SERIALIZE_OPTS = ['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'json-ld']
    LS_OPTS = ['ontologies', 'classes', 'properties', 'concepts']
    TREE_OPTS = ['classes', 'properties', 'concepts']
    GET_OPTS = ['ontology', 'class', 'property', 'concept']
    FILE_OPTS = ['rename', 'delete']
    IMPORT_OPTS = ['uri', 'file',  'repo', 'starter-pack', ]
    VISUALIZE_OPTS = []

    def __init__(self, uri=None):
        """
        self.current = {'file' : filename, 'fullpath' : fullpath, 'graph': g}
        self.currentEntity = {'name' : obj.locale or obj.uri, 'object' : obj, 'type' : 'class'}
                                                                    # or 'property' or 'concept'
        """
        # init repo if necessary
        manager.get_or_create_home_repo()
        # useful vars
        self.LOCAL = ONTOSPY_LOCAL
        self.LOCAL_MODELS = manager.get_home_location()
        self.all_ontologies = manager.get_localontologies()
        self.current = None
        self.currentEntity = None
        if uri:
            self._load_ontology(uri, preview_mode=True)
        cmd.Cmd.__init__(self)

    # BASE CLASSE OVERRIDES:
    # --------

    def emptyline(self):
        """ override default behaviour of running last command """
        pass

    def print_topics(self, header, cmds, cmdlen, maxcol):
        """Override 'print_topics' so that you can exclude EOF and shell.
            2016-02-12: added to test, copied from
            https://github.com/xlcnd/isbntools/blob/master/isbntools/bin/repl.py
        """
        if header:
            if cmds:
                self.stdout.write("%s\n" % str(header))
                if self.ruler:
                    self.stdout.write("%s\n" % str(self.ruler * len(header)))
                self.columnize(cmds, maxcol - 1)
                self.stdout.write("\n")

    def default(self, line):
        "default message when a command is not recognized"
        foo = ["Don't recognize that command. Try 'help' for some suggestions.",
               "That looks like the wrong command", "Are you sure you mean that? Try 'help' for some suggestions."]
        self._print(random.choice(foo))

    # HELPER METHODS
    # --------

    def _print(self, ms, style="TIP"):
        """ abstraction for managing color printing """
        styles1 = {'IMPORTANT': Style.BRIGHT,
                   'TIP': Style.DIM,
                   'URI': Style.BRIGHT,
                   'TEXT': Fore.GREEN,
                   'MAGENTA': Fore.MAGENTA,
                   'BLUE': Fore.BLUE,
                   'GREEN': Fore.GREEN,
                   'RED': Fore.RED,
                   'DEFAULT': Style.DIM,
                   }
        try:
            printInfo(styles1[style] + ms + Style.RESET_ALL)
        except:
            printInfo(styles1['DEFAULT'] + ms + Style.RESET_ALL)

    def _printM(self, messages):
        """print a list of strings - for the mom used only by stats printout"""
        if len(messages) == 2:
            printInfo(Style.BRIGHT + messages[0] + Style.RESET_ALL +
                  Fore.BLUE + messages[1] + Style.RESET_ALL)
        else:
            printInfo("Not implemented")

    def _joinedQnames(self, _list):
        """util for returning a string joinin names of entities *used only in info command*"""
        try:
            s = "; ".join([p.qname for p in _list])
        except:
            s = "; ".join([p for p in _list])
        return s

    def _clear_screen(self):
        """ http://stackoverflow.com/questions/18937058/python-clear-screen-in-shell """
        if platform.system() == "Windows":
            tmp = os.system('cls')  # for window
        else:
            tmp = os.system('clear')  # for Linux
        return True

    def _printTriples(self, entity):
        """ display triples """
        self._print("----------------", "TIP")
        self._print(unicode(entity.uri), "IMPORTANT")
        for x in entity.triples:
            self._print("=> " + unicode(x[1]), "MAGENTA")
            self._print(".... " + unicode(x[2]), "GREEN")
        self._print("----------------", "TIP")

    def _print_entity_intro(self, g=None, entity=None, first_time=True):
        """after a selection, prints on screen basic info about onto or entity, plus change prompt
        2015-10-18: removed the sound
        2016-01-18: entity is the shell wrapper around the ontospy entity
        """
        if entity:
            self._clear_screen()
            obj = entity['object']
            self._print("Loaded %s: <%s>" % (entity['type'].capitalize(), str(obj.uri)), "TIP")
            self._print("----------------", "TIP")
            # self._print(obj.bestDescription(), "TEXT")
            if first_time:
                self.prompt = _get_prompt(self.current['file'], self.currentEntity)
        elif g:
            self._printDescription(False)
            if first_time:
                self.prompt = _get_prompt(self.current['file'])

    def _printStats(self, graph, hrlinetop=False):
        """ shotcut to pull out useful info for interactive use
        2016-05-11: note this is a local version of graph.printStats()
        """
        if hrlinetop:
            self._print("----------------", "TIP")
        self._print("Ontologies......: %d" % len(graph.all_ontologies), "TIP")
        self._print("Classes.........: %d" % len(graph.all_classes), "TIP")
        self._print("Properties......: %d" % len(graph.all_properties), "TIP")
        self._print("..annotation....: %d" % len(graph.all_properties_annotation), "TIP")
        self._print("..datatype......: %d" % len(graph.all_properties_datatype), "TIP")
        self._print("..object........: %d" % len(graph.all_properties_object), "TIP")
        self._print("Concepts(SKOS)..: %d" % len(graph.all_skos_concepts), "TIP")
        self._print("----------------", "TIP")

    def _printDescription(self, hrlinetop=True):
        """generic method to print out a description"""
        if hrlinetop:
            self._print("----------------")
        NOTFOUND = "[not found]"
        if self.currentEntity:
            obj = self.currentEntity['object']
            label = obj.bestLabel() or NOTFOUND
            description = obj.bestDescription() or NOTFOUND
            printInfo(Style.BRIGHT + "OBJECT TYPE: " + Style.RESET_ALL +
                  Fore.BLACK + uri2niceString(obj.rdftype) + Style.RESET_ALL)
            printInfo(Style.BRIGHT + "URI        : " + Style.RESET_ALL +
                  Fore.GREEN + "<" + unicode(obj.uri) + ">" + Style.RESET_ALL)
            printInfo(Style.BRIGHT + "TITLE      : " + Style.RESET_ALL +
                  Fore.BLACK + label + Style.RESET_ALL)
            printInfo(Style.BRIGHT + "DESCRIPTION: " + Style.RESET_ALL +
                  Fore.BLACK + description + Style.RESET_ALL)

        else:
            self._clear_screen()
            self._print("Graph: <" + self.current['fullpath'] + ">", 'TIP')
            self._print("----------------", "TIP")
            self._printStats(self.current['graph'])
            for obj in self.current['graph'].all_ontologies:
                printInfo(Style.BRIGHT + "Ontology URI: " + Style.RESET_ALL +
                      Fore.RED + "<%s>" % str(obj.uri) + Style.RESET_ALL)
                # self._print("==> Ontology URI: <%s>" % str(obj.uri), "IMPORTANT")
                # self._print("----------------", "TIP")
                label = obj.bestLabel() or NOTFOUND
                description = obj.bestDescription() or NOTFOUND
                printInfo(Style.BRIGHT + "Title       : " + Style.RESET_ALL +
                      Fore.BLACK + label + Style.RESET_ALL)
                printInfo(Style.BRIGHT + "Description : " + Style.RESET_ALL +
                      Fore.BLACK + description + Style.RESET_ALL)
        self._print("----------------", "TIP")
        # self._print("----------------", "TIP")

    def _printTaxonomy(self, hrlinetop=True):
        """
        print a local taxonomy for the object
        """
        if not self.currentEntity:  # ==> ontology level
            return
        if hrlinetop:
            self._print("----------------")
        self._print("TAXONOMY:", "IMPORTANT")
        x = self.currentEntity['object']
        parents = x.parents()

        if not parents:
            if self.currentEntity['type'] == 'class':
                self._print("owl:Thing")
            elif self.currentEntity['type'] == 'property':
                self._print("RDF:Property")
            elif self.currentEntity['type'] == 'concept':
                self._print("SKOS:Concept")
            else:
                pass
        else:
            for p in parents:
                self._print(p.qname)
        self._print("..." + x.qname, "TEXT")
        for c in x.children():
            self._print("......" + c.qname)
        self._print("----------------")

    def _printClassDomain(self, hrlinetop=True, print_inferred=False):
        """
        print more informative stats about the object
        2016-06-14: added inferred option
        """
        if not self.currentEntity:  # ==> ontology level
            return
        x = self.currentEntity['object']
        if self.currentEntity['type'] == 'class':
            if hrlinetop:
                self._print("----------------")
            self._print("DOMAIN OF:", "IMPORTANT")
            self._print("[%d] Explicitly declared" % len(x.domain_of), "IMPORTANT")
            for i in x.domain_of:
                if i.ranges:
                    ranges = ",".join([y.qname if hasattr(y, "qname") else str(y)
                                       for y in i.ranges])
                else:
                    ranges = "owl:Thing"
                    # print( Style.RESET_ALL + " => " + Fore.MAGENTA +
                printInfo(Fore.GREEN + x.qname + Style.RESET_ALL + " => " + Fore.MAGENTA +
                      i.qname + Style.RESET_ALL + " => " + Style.DIM + ranges +
                      Style.RESET_ALL)

            # inferred stuff
            if print_inferred:
                for _dict in x.domain_of_inferred:
                    _class = list(_dict.items())[0][0]
                    _propslist = list(_dict.items())[0][1]
                    if _class.id != x.id and len(_propslist):  # print only inferred properties
                        self._print("[%d] Inherited from [%s]" % (len(_propslist), _class.qname),
                                    "IMPORTANT")
                        for i in _propslist:
                            if i.ranges:
                                ranges = ",".join([y.qname if hasattr(y, "qname")
                                                   else str(y) for y in i.ranges])
                            else:
                                ranges = "owl:Thing"
                                # print(Style.RESET_ALL + " => " + Fore.MAGENTA +
                            printInfo(Fore.GREEN + x.qname + Style.RESET_ALL + " => " + Fore.MAGENTA +
                                  i.qname + Style.RESET_ALL + " => " + Style.DIM +
                                  ranges + Style.RESET_ALL)

            self._print("----------------")
        return

    def _printClassRange(self, hrlinetop=True, print_inferred=False):
        """
        print(more informative stats about the object)
        2016-06-14: added inferred option
        """
        if not self.currentEntity:  # ==> ontology level
            return
        x = self.currentEntity['object']
        if self.currentEntity['type'] == 'class':
            if hrlinetop:
                self._print("----------------")
            self._print("RANGE OF:", "IMPORTANT")
            self._print("[%d] Explicitly declared" % len(x.range_of), "IMPORTANT")
            for i in x.range_of:
                if i.domains:
                    domains = ",".join([y.qname if hasattr(y, "qname") else str(y)
                                        for y in i.domains])
                else:
                    domains = "owl:Thing"
                printInfo(Style.DIM + domains + Style.RESET_ALL + " => " + Fore.MAGENTA + i.qname +
                      Style.RESET_ALL + " => " + Fore.GREEN + x.qname + Style.RESET_ALL)

            # inferred stuff
            if print_inferred:
                for _dict in x.range_of_inferred:
                    _class = list(_dict.items())[0][0]
                    _propslist = list(_dict.items())[0][1]
                    if _class.id != x.id and len(_propslist):  # print only inferred properties
                        self._print("[%d] Inherited from [%s]" % (len(_propslist), _class.qname),
                                    "IMPORTANT")
                        for i in _propslist:
                            if i.domains:
                                domains = ",".join(
                                    [y.qname if hasattr(y, "qname") else str(y) for y in i.domains])
                            else:
                                domains = "owl:Thing"
                            printInfo(Style.DIM + domains + Style.RESET_ALL + " => " + Fore.MAGENTA +
                                  i.qname + Style.RESET_ALL + " => " + Fore.GREEN + x.qname + Style.RESET_ALL)

            self._print("----------------")
        return

    def _printPropertyDomainRange(self, hrlinetop=True):
        """
        print(more informative stats about the object)
        """
        if not self.currentEntity:  # ==> ontology level
            return
        x = self.currentEntity['object']
        if self.currentEntity['type'] == 'property':
            if hrlinetop:
                self._print("----------------")
            self._print("USAGE:", "IMPORTANT")
            domains = x.domains
            ranges = x.ranges
            if x.domains:
                for d in x.domains:
                    # for domain/ranges which are not declared classes
                    if hasattr(d, "qname"):
                        _name = d.qname
                    else:
                        _name = str(d)
                    self._print(_name)
            else:
                self._print("owl:Thing")
            self._print("  " + x.qname, "TEXT")
            if x.ranges:
                for d in x.ranges:
                    # for domain/ranges which are not declared classes
                    if hasattr(d, "qname"):
                        _name = d.qname
                    else:
                        _name = str(d)
                    self._print("  " + "   => " + _name)
            else:
                self._print("  " + "   => " + "owl:Thing")
            self._print("----------------")
        return

    def _printInstances(self, hrlinetop=True):
        """
        print(more informative stats about the object)
        """
        if not self.currentEntity:  # ==> ontology level
            return
        x = self.currentEntity['object']
        if self.currentEntity['type'] == 'class':
            if hrlinetop:
                self._print("----------------")
            self._print("INSTANCES: [%d]" % len(x.instances, "IMPORTANT"))
            for i in x.instances:
                self._print(i.qname)
            self._print("----------------")
        return

    def _printSourceCode(self, hrlinetop=True):
        """
        print(more informative stats about the object)
        """
        if not self.currentEntity:  # ==> ontology level
            return
        x = self.currentEntity['object']
        if hrlinetop:
            self._print("----------------")

        self._print("Source:", "IMPORTANT")
        self.do_serialize("turtle")
        self._print("----------------")

        return

    def _selectFromList(self, _list, using_pattern=True, objtype=None):
        """
        Generic method that lets users pick an item from a list via input
        *using_pattern* flag to know if we're showing all choices or not
        Note: the list items need to be Ontospy entities.
        <objtype>: if specified, it allows incremental search by keeping specifying a
        different pattern.
        """
        if not _list:
            self._print("No matching items.", "TIP")
            return None
        if using_pattern and len(_list) == 1:  # removed
            pass
            # return _list[0]
        if using_pattern:
            self._print("%d matching items: \n--------------" % len(_list), "TIP")
        else:
            self._print("%d items available: \n--------------" % len(_list), "TIP")
        counter = 1
        _temp = []
        for el in _list:
            if hasattr(el, 'qname'):
                _temp += [Fore.BLUE + Style.BRIGHT + "[%d] " %
                          counter + Style.RESET_ALL + str(el.qname)]
            elif hasattr(el, 'uri'):
                _temp += [Fore.BLUE + Style.BRIGHT + "[%d] " %
                          counter + Style.RESET_ALL + str(el.uri)]
            else:
                _temp += [Fore.BLUE + Style.BRIGHT + "[%d] " % counter + Style.RESET_ALL + str(el)]
            counter += 1
        pprint2columns(_temp)

        self._print("--------------")
        self._print("Please select one option by entering its number, or a keyword to filter: ")
        var = input()
        if var == "":
            return None
        elif var.isdigit():
            try:
                var = int(var)
                return _list[var-1]
            except:
                self._print("Selection not valid")
                return None
        elif objtype:
            # continuos patter matching on list (only for certain object types)
            if objtype == 'ontology':
                self._select_ontology(var)
            elif objtype == 'class':
                self._select_class(var)
            elif objtype == 'property':
                self._select_property(var)
            elif objtype == 'concept':
                self._select_concept(var)
            return

    def _next_ontology(self):
        """Dynamically retrieves the next ontology in the list"""
        currentfile = self.current['file']
        try:
            idx = self.all_ontologies.index(currentfile)
            return self.all_ontologies[idx+1]
        except:
            return self.all_ontologies[0]

    # MAIN METHODS
    # --------

    def _load_ontology(self, filename, preview_mode=False):
        """
        Loads an ontology

        Unless preview_mode=True, it is always loaded from the local repository
        note: if the ontology does not have a cached version, it is created

        preview_mode: used to pass a URI/path to be inspected without saving it locally
        """
        if not preview_mode:
            fullpath = self.LOCAL_MODELS + filename
            g = manager.get_pickled_ontology(filename)
            if not g:
                g = manager.do_pickle_ontology(filename)
        else:
            fullpath = filename
            filename = os.path.basename(os.path.normpath(fullpath))
            g = Ontospy(fullpath, verbose=True)
        self.current = {'file': filename, 'fullpath': fullpath, 'graph': g}
        self.currentEntity = None
        self._print_entity_intro(g)

    def _select_ontology(self, line):
        """try to select an ontology NP: the actual load from FS is in <_load_ontology> """
        try:
            var = int(line)  # it's a string
            if var in range(1, len(self.all_ontologies)+1):
                self._load_ontology(self.all_ontologies[var-1])
        except ValueError:
            out = []
            for each in self.all_ontologies:
                if line in each:
                    out += [each]
            choice = self._selectFromList(out, line, "ontology")
            if choice:
                self._load_ontology(choice)

    def _select_class(self, line):
        """
        try to match a class and load it from the graph
        NOTE: the g.get_class(pattern) method does the heavy lifting
        """
        g = self.current['graph']
        if not line:
            out = g.all_classes
            using_pattern = False
        else:
            using_pattern = True
            if line.isdigit():
                line = int(line)
            out = g.get_class(line)
        if out:
            if type(out) == type([]):
                choice = self._selectFromList(out, using_pattern, "class")
                if choice:
                    self.currentEntity = {'name': choice.locale or choice.uri,
                                          'object': choice, 'type': 'class'}
            else:
                self.currentEntity = {'name': out.locale or out.uri, 'object': out, 'type': 'class'}
            # ..finally:
            if self.currentEntity:
                self._print_entity_intro(entity=self.currentEntity)

        else:
            printInfo("not found")

    def _select_property(self, line):
        """try to match a property and load it"""
        g = self.current['graph']
        if not line:
            out = g.all_properties
            using_pattern = False
        else:
            using_pattern = True
            if line.isdigit():
                line = int(line)
            out = g.get_property(line)
        if out:
            if type(out) == type([]):
                choice = self._selectFromList(out, using_pattern, "property")
                if choice:
                    self.currentEntity = {'name': choice.locale or choice.uri,
                                          'object': choice, 'type': 'property'}

            else:
                self.currentEntity = {'name': out.locale or out.uri,
                                      'object': out, 'type': 'property'}

            # ..finally:
            if self.currentEntity:
                self._print_entity_intro(entity=self.currentEntity)
        else:
            printInfo("not found")

    def _select_concept(self, line):
        """try to match a class and load it"""
        g = self.current['graph']
        if not line:
            out = g.all_skos_concepts
            using_pattern = False
        else:
            using_pattern = True
            if line.isdigit():
                line = int(line)
            out = g.get_skos(line)
        if out:
            if type(out) == type([]):
                choice = self._selectFromList(out, using_pattern, "concept")
                if choice:
                    self.currentEntity = {'name': choice.locale or choice.uri,
                                          'object': choice, 'type': 'concept'}
            else:
                self.currentEntity = {'name': out.locale or out.uri,
                                      'object': out, 'type': 'concept'}
            # ..finally:
            if self.currentEntity:
                self._print_entity_intro(entity=self.currentEntity)

        else:
            printInfo("not found")

    def _delete_file(self, line=""):
        """	Delete an ontology
            2016-04-11: not a direct command anymore """

        if not self.all_ontologies:
            self._help_nofiles()

        else:
            out = []
            for each in self.all_ontologies:
                if line in each:
                    out += [each]
            choice = self._selectFromList(out, line)
            if choice:
                fullpath = self.LOCAL_MODELS + "/" + choice
                if os.path.isfile(fullpath):

                    self._print("--------------")
                    self._print("Are you sure? [Y/N]")
                    var = input()
                    if var == "y" or var == "Y":
                        os.remove(fullpath)
                        manager.del_pickled_ontology(choice)
                        self._print("<%s> was deleted succesfully." % choice)
                        self.all_ontologies = manager.get_localontologies()
                    else:
                        return

                else:
                    self._print("File not found.")
                # delete
                if self.current and self.current['fullpath'] == fullpath:
                    self.current = None
                    self.currentEntity = None
                    self.prompt = _get_prompt()

        return

    def _rename_file(self, line=""):
        """Rename an ontology
            2016-04-11: not a direct command anymore """

        if not self.all_ontologies:
            self._help_nofiles()
        else:
            out = []
            for each in self.all_ontologies:
                if line in each:
                    out += [each]
            choice = self._selectFromList(out, line)
            if choice:
                fullpath = self.LOCAL_MODELS + "/" + choice
                printDebug(fullpath)
                if os.path.isfile(fullpath):

                    self._print("--------------")
                    self._print("Please enter a new name for <%s>, including the extension (blank=abort)"
                                % choice)
                    var = input()
                    if var:
                        try:
                            os.rename(fullpath, self.LOCAL_MODELS + "/" + var)
                            manager.rename_pickled_ontology(choice, var)
                            self._print("<%s> was renamed succesfully." % choice)
                            self.all_ontologies = manager.get_localontologies()
                        except:
                            self._print("Not a valid name. An error occurred.")
                            return
                    else:
                        return

                else:
                    self._print("File not found.")
                # delete
                if self.current and self.current['fullpath'] == fullpath:
                    self.current = None
                    self.currentEntity = None
                    self.prompt = _get_prompt()

        return

    # COMMANDS
    # --------
    # NOTE: all commands should start with 'do_' and must pass 'line'

    def do_ls(self, line):
        """Shows entities of a given kind."""
        opts = self.LS_OPTS
        line = line.split()
        _pattern = ""

        if len(line) == 0:
            # default contextual behaviour [2016-03-01]
            if not self.current:
                line = ["ontologies"]
            elif self.currentEntity:
                self.do_info("")
                return
            else:
                line = ["classes"]

        if (not line) or (line[0] not in opts):
            self.help_ls()
            return
            # self._print("Usage: ls [%s]" % "|".join([x for x in opts]))

        elif line[0] == "ontologies":
            if not self.all_ontologies:
                self._help_nofiles()
            else:
                self._select_ontology(_pattern)

        elif line[0] in opts and not self.current:
            self._help_noontology()
            return

        elif line[0] == "classes":
            g = self.current['graph']

            if g.all_classes:
                self._select_class(_pattern)
            else:
                self._print("No classes available.")

        elif line[0] == "properties":
            g = self.current['graph']
            if g.all_properties:
                self._select_property(_pattern)
            else:
                self._print("No properties available.")

        elif line[0] == "concepts":
            g = self.current['graph']
            if g.all_skos_concepts:
                self._select_concept(_pattern)
            else:
                self._print("No concepts available.")

        else:  # should never arrive here
            pass

    def do_tree(self, line):
        """Shows entities of a given kind."""
        opts = self.TREE_OPTS
        line = line.split()
        _pattern = ""

        if not self.current:
            self._help_noontology()
            return

        if len(line) == 0:
            # default contextual behaviour [2016-03-01]
            line = ["classes"]

        if line[0] not in opts:
            self.help_tree()
            return

        elif line[0] == "classes":
            g = self.current['graph']
            if g.all_classes:
                g.printClassTree(showids=False, labels=False, showtype=True)
                self._print("----------------", "TIP")
            else:
                self._print("No classes available.")

        elif line[0] == "properties":
            g = self.current['graph']
            if g.all_properties:
                g.printPropertyTree(showids=False, labels=False, showtype=True)
            else:
                self._print("No properties available.")

        elif line[0] == "concepts":
            g = self.current['graph']
            if g.all_skos_concepts:
                g.printSkosTree(showids=False, labels=False, showtype=True)
            else:
                self._print("No concepts available.")

        else:  # should never arrive here
            pass

    def do_get(self, line):
        """Finds entities matching a given string pattern. \nOptions: [ ontologies | classes | properties | concepts ]"""
        line = line.split()
        _pattern = ""
        if len(line) > 1:
            _pattern = line[1]
        opts = self.GET_OPTS

        if (not line) or (line[0] not in opts) or (not _pattern):
            self.help_get()
            return
            # self._print("Usage: get [%s] <name>" % "|".join([x for x in opts]))

        elif line[0] == "ontology":
            if not self.all_ontologies:
                self._help_nofiles()
            else:
                self._select_ontology(_pattern)

        elif line[0] in opts and not self.current:
            self._help_noontology()
            return

        elif line[0] == "class":
            g = self.current['graph']
            if g.all_classes:
                self._select_class(_pattern)
            else:
                self._print("No classes available.")

        elif line[0] == "property":
            g = self.current['graph']
            if g.all_properties:
                self._select_property(_pattern)
            else:
                self._print("No properties available.")

        elif line[0] == "concept":
            g = self.current['graph']
            if g.all_skos_concepts:
                self._select_concept(_pattern)
            else:
                self._print("No concepts available.")

        else:  # should never arrive here
            pass

    def do_info(self, line):
        """Inspect the current entity and display a nice summary of key properties"""
        # opts = [ 'namespaces', 'description', 'overview', 'toplayer', 'parents', 'children', 'stats', 'triples' ]
        opts = self.INFO_OPTS

        if not self.current:
            self._help_noontology()
            return

        line = line.split()
        g = self.current['graph']

        # get arg, or default to 'overview'
        if not line:
            self._printDescription()
            self._printTaxonomy(False)
            self._printClassDomain(False)
            self._printClassRange(False)
            self._printPropertyDomainRange(False)
            # self._printSourceCode(False)
            if self.currentEntity and self.currentEntity['type'] == 'class':
                self._print("Tip: type 'info inferred_usage' to show inherited properties\n----------------")

        elif line[0] == "inferred_usage":
            if self.currentEntity:  # @todo only for classes?
                self._printDescription()
                self._printTaxonomy(False)
                self._printClassDomain(False, True)
                self._printClassRange(False, True)
                self._printPropertyDomainRange(False)
            # self._printSourceCode(False)
            return

        elif line[0] == "toplayer":
            if g.toplayer_classes:
                self._print("Top Classes\n----------------", "IMPORTANT")
            for x in g.toplayer_classes:
                self._print(x.qname)
            if g.toplayer_properties:
                self._print("\nTop Properties\n----------------", "IMPORTANT")
                for x in g.toplayer_properties:
                    self._print(x.qname)
            if g.toplayer_skos:
                self._print("\nTop Concepts (SKOS)\n----------------", "IMPORTANT")
                for x in g.toplayer_skos:
                    self._print(x.qname)

        elif line[0] == "namespaces":
            for x in self.current['graph'].namespaces:
                self._print("@prefix %s: <%s> ." % (x[0], x[1]))

        elif line[0] == "parents":
            if self.currentEntity and self.currentEntity['object'].parents():
                for x in self.currentEntity['object'].parents():
                    self._print(x.qname)
            else:
                self._print("No parents. This is a top level entity.")

        elif line[0] == "children":
            if self.currentEntity and self.currentEntity['object'].children():
                for x in self.currentEntity['object'].children():
                    self._print(x.qname)
            else:
                self._print("No children. This is a leaf node.")

        elif line[0] == "ancestors":
            if self.currentEntity and self.currentEntity['object'].ancestors():
                for x in self.currentEntity['object'].ancestors():
                    self._print(x.qname)
            else:
                self._print("No ancestors. This is a top level entity.")

        elif line[0] == "descendants":
            if self.currentEntity and self.currentEntity['object'].descendants():
                for x in self.currentEntity['object'].descendants():
                    self._print(x.qname)
            else:
                self._print("No descendants. This is a leaf node.")

            return

    def do_visualize(self, line):
        """Visualize an ontology - ie wrapper for export command"""

        if not self.current:
            self._help_noontology()
            return

        line = line.split()

        try:
            # from ..viz.builder import action_visualize
            from ..ontodocs.builder import action_visualize
        except:
            self._print("This command requires the ontodocs package: `pip install ontodocs`")
            return

        import webbrowser
        url = action_visualize(args=self.current['file'], fromshell=True)
        if url:
            webbrowser.open(url)
        return

    def do_import(self, line):
        """Import an ontology"""

        line = line.split()

        if line and line[0] == "starter-pack":
            actions.action_bootstrap()

        elif line and line[0] == "uri":
            self._print(
                "------------------\nEnter a valid graph URI: (e.g. http://www.w3.org/2009/08/skos-reference/skos.rdf)")
            var = input()
            if var:
                if var.startswith("http"):
                    try:
                        actions.action_import(var)
                    except:
                        self._print(
                            "OPS... An Unknown Error Occurred - Aborting installation of <%s>" % var)
                else:
                    self._print("Not valid. TIP: URIs should start with 'http://'")

        elif line and line[0] == "file":
            self._print(
                "------------------\nEnter a full file path: (e.g. '/Users/mike/Desktop/journals.ttl')")
            var = input()
            if var:
                try:
                    actions.action_import(var)
                except:
                    self._print(
                        "OPS... An Unknown Error Occurred - Aborting installation of <%s>" % var)

        elif line and line[0] == "repo":
            actions.action_webimport()

        else:
            self.help_import()

        self.all_ontologies = manager.get_localontologies()
        return

    def do_file(self, line):
        """PErform some file operation"""
        opts = self.FILE_OPTS

        if not self.all_ontologies:
            self._help_nofiles()
            return

        line = line.split()

        if not line or line[0] not in opts:
            self.help_file()
            return

        if line[0] == "rename":
            self._rename_file()
        elif line[0] == "delete":
            self._delete_file()
        else:
            return

    def do_serialize(self, line):
        """Serialize an entity into an RDF flavour"""
        opts = self.SERIALIZE_OPTS

        if not self.current:
            self._help_noontology()
            return

        line = line.split()
        g = self.current['graph']

        if not line:
            line = ['turtle']

        if line[0] not in opts:
            self.help_serialize()
            return

        elif self.currentEntity:
            self.currentEntity['object'].printSerialize(line[0])

        else:
            self._print(g.rdf_source(format=line[0]))
            # 2016-05-27: was like this before
            # for o in g.all_ontologies:
            # 	o.printSerialize(line[0])

    def do_next(self, line):
        """Jump to the next entities (ontology, class or property) depending on context"""
        if not self.current:
            printInfo("Please select an ontology first. E.g. use the 'ls ontologies' or 'get ontology <name>' commands.")
        elif self.currentEntity:
            g = self.current['graph']
            if self.currentEntity['type'] == 'class':
                nextentity = g.nextClass(self.currentEntity['object'].uri)
                self._select_class(str(nextentity.uri))
            elif self.currentEntity['type'] == 'property':
                nextentity = g.nextProperty(self.currentEntity['object'].uri)
                self._select_property(str(nextentity.uri))
            elif self.currentEntity['type'] == 'concept':
                nextentity = g.nextConcept(self.currentEntity['object'].uri)
                self._select_concept(str(nextentity.uri))
            else:
                printInfo("Not implemented")
        else:
            if len(self.all_ontologies) > 1:
                nextonto = self._next_ontology()
                self._load_ontology(nextonto)
            else:
                self._print("Only one ontology available in repository.")

    def do_back(self, line):
        "Go back one step. From entity => ontology; from ontology => ontospy top level."
        if self.currentEntity:
            self.currentEntity = None
            self.prompt = _get_prompt(self.current['file'])
        else:
            self.current = None
            self.prompt = _get_prompt()

    def do_quit(self, line):
        "Quit: exit the Ontospy shell"
        self._clear_screen()
        return True

    def do_zen(self, line):
        """Inspiring quotes for the working ontologist"""
        _quote = random.choice(QUOTES)
        # print(_quote['source'])
        printInfo(Style.DIM + unicode(_quote['text']))
        printInfo(Style.BRIGHT + unicode(_quote['source']) + Style.RESET_ALL)

    # 2016-02-12: method taken from https://github.com/xlcnd/isbntools/blob/master/isbntools/bin/repl.py
    # 2016-04-25: hidden
    def _do_shell(self, line):
        """Send a command to the Unix shell.\n==> Usage: shell ls ~"""
        if not line:
            return
        sp = Popen(line,
                   shell=True,
                   stdin=PIPE,
                   stdout=PIPE,
                   stderr=PIPE,
                   close_fds=not WINDOWS)
        (fo, fe) = (sp.stdout, sp.stderr)
        if PY2:
            out = fo.read().strip(EOL)
            err = fe.read().strip(EOL)
        else:
            out = fo.read().decode("utf-8")
            err = fe.read().decode("utf-8")
        if out:
            printInfo(out)
            return
        if err:
            printInfo(err.replace('isbn_', ''))

    # HELP METHODS
    # --------

    def help_ls(self):
        txt = "List available graphs or entities .\n"
        txt += "==> Usage: ls [%s]" % "|".join([x for x in self.LS_OPTS])
        txt += "\n\nNote: ls is contextual. If you do not pass it any argument, it returns info based on the currently active object.\n"
        self._print(txt)

    def help_tree(self):
        txt = "Print the type hierarchy for an entity type.\n"
        txt += "==> Usage: tree [%s]" % "|".join([x for x in self.TREE_OPTS])
        # txt += "\n\nNote: tree is contextual. If you do not pass it any argument, it returns info based on the currently active object.\n"
        self._print(txt)

    def help_import(self):
        txt = "Import an ontology from a remote repository or directory.\n"
        txt += "==> Usage: import [%s]" % "|".join([x for x in self.IMPORT_OPTS])
        self._print(txt)

    def help_visualize(self):
        txt = "Visualize the currenlty selected ontology using an HTML template.\n"
        txt += "==> Usage: visualize "
        self._print(txt)

    def help_file(self):
        txt = "Perform some operations on the files in the local repository.\n"
        txt += "==> Usage: file [%s]" % "|".join([x for x in self.FILE_OPTS])
        self._print(txt)

    def help_serialize(self):
        txt = "Serialize an entity into an RDF flavour.\n"
        txt += "==> Usage: serialize [%s]" % "|".join([x for x in self.SERIALIZE_OPTS])
        self._print(txt)

    def help_get(self):
        txt = "Finds entities matching a given string pattern.\n"
        txt += "==> Usage: get [%s] <name>" % "|".join([x for x in self.GET_OPTS])
        self._print(txt)

    def help_info(self):
        txt = "Display information about an entity e.g. ontology, class etc..\n"
        txt += "==> Usage: info OR info [%s]" % "|".join([x for x in self.INFO_OPTS])
        self._print(txt)

    def _help_noontology(self):
        """starts with underscore so that it doesnt appear with help methods"""
        txt = "No graph selected. Please load a graph first.\n"
        txt += "==> E.g. use the 'ls ontologies' or 'get ontology <name>' commands."
        self._print(txt)

    def _help_nofiles(self):
        """starts with underscore so that it doesnt appear with help methods"""
        txt = "No files available in your local repository.\n"
        txt += "==> Use the 'import starter-pack' command to get started."
        self._print(txt)

    # AUTOCOMPLETE METHODS
    # --------

    def complete_ls(self, text, line, begidx, endidx):
        """completion for ls command"""

        options = self.LS_OPTS

        if not text:
            completions = options
        else:
            completions = [f
                           for f in options
                           if f.startswith(text)
                           ]
        return completions

    def complete_tree(self, text, line, begidx, endidx):
        """completion for ls command"""

        options = self.TREE_OPTS

        if not text:
            completions = options
        else:
            completions = [f
                           for f in options
                           if f.startswith(text)
                           ]
        return completions

    def complete_get(self, text, line, begidx, endidx):
        """completion for find command"""

        options = self.GET_OPTS

        if not text:
            completions = options
        else:
            completions = [f
                           for f in options
                           if f.startswith(text)
                           ]
        return completions

    def complete_info(self, text, line, begidx, endidx):
        """completion for info command"""

        opts = self.INFO_OPTS

        if not text:
            completions = opts
        else:
            completions = [f
                           for f in opts
                           if f.startswith(text)
                           ]
        return completions

    def complete_import(self, text, line, begidx, endidx):
        """completion for serialize command"""

        opts = self.IMPORT_OPTS

        if not text:
            completions = opts
        else:
            completions = [f
                           for f in opts
                           if f.startswith(text)
                           ]
        return completions

    def complete_serialize(self, text, line, begidx, endidx):
        """completion for serialize command"""

        opts = self.SERIALIZE_OPTS

        if not text:
            completions = opts
        else:
            completions = [f
                           for f in opts
                           if f.startswith(text)
                           ]
        return completions

    def complete_visualize(self, text, line, begidx, endidx):
        """completion for file command"""

        opts = self.VISUALIZE_OPTS

        if not text:
            completions = opts
        else:
            completions = [f
                           for f in opts
                           if f.startswith(text)
                           ]
        return completions

    def complete_file(self, text, line, begidx, endidx):
        """completion for file command"""

        opts = self.FILE_OPTS

        if not text:
            completions = opts
        else:
            completions = [f
                           for f in opts
                           if f.startswith(text)
                           ]
        return completions


def main():
    """ standalone line script """

    printInfo("Ontospy " + VERSION)

    Shell()._clear_screen()
    printInfo(Style.BRIGHT + "** Ontospy Interactive Ontology Browser " + VERSION + " **" + Style.RESET_ALL)
    # manager.get_or_create_home_repo()
    Shell().cmdloop()
    raise SystemExit(1)


if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
