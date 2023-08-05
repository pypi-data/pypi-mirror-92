from sailboat.plugins import Plugin

class Tiller(Plugin):
	_type = "command"
	description = "echo a test string."
	setup = {
		'string::str':'String to echo: '
	}

	def add(self):
		print('\n\n\tAdded!\n\n')
	
	def run(self):
		print(self.getData('string'))