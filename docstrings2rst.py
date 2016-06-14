#!/usr/bin/python
# coding:utf8
from theTaleApi import theTaleApi
import inspect
import re
from sys import argv
functions = inspect.getmembers(theTaleApi, predicate=inspect.ismethod)
first = True
allow = ['__init__']
with open('{}/doc.rst'.format(argv[1]), 'w') as f:
	for name, func in functions:
		if not name.startswith('_') or name in allow:
			if not first:
				f.seek(-1, 1)
			else:
				first = False
			print(name)
			doc = func.__doc__
			for docstring in doc.split('\n'):
				if docstring.startswith('\t\t.. function::'):
					docstring = re.sub(r'\t\t(\.\. function\:\: .+\(.*\).*)', r'\1\n', docstring)
				else:
					docstring = docstring.replace('\t\t', '\t')
				f.write(docstring + '\n')
