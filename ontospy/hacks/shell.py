
# docs:
# https://docs.python.org/2/library/cmd.html
# http://pymotw.com/2/cmd/

import cmd
import ontospy2


class HelloWorld(cmd.Cmd):
	"""Simple command processor example."""

	prompt = '<OntoSPy>: '
	intro = "Ontology is a work of love."

	doc_header = 'doc_header'
	misc_header = 'misc_header'
	undoc_header = 'undoc_header'
	
	ruler = '-'
	
	# NOTE: all commands should start with 'do_' and must pass 'line'
	
	def do_load(self, line):
		"Test of loading the foaf ontology"
		DEFAULT_ONTO = "http://xmlns.com/foaf/0.1/"
		g = ontospy3.Graph(DEFAULT_ONTO)
		ontologies = g.scan()
		for o in ontologies:
			print "Ontology URI:", o.uri
			print "Annotations:", o.annotations
	
	def do_prompt(self, line):
		"Change the interactive prompt"
		self.prompt = line + ': '

	def default(self, line):
		"default message when a command is not recognized"
		print "Wow first time I hear that"

	def do_EOF(self, line):
		return True

if __name__ == '__main__':
	HelloWorld().cmdloop()