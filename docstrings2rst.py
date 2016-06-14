#!/usr/bin/python
# coding:utf8
from theTaleApi import theTaleApi
import inspect
import re
functions = inspect.getmembers(theTaleApi, predicate=inspect.ismethod)
first = True
with open('./docs/source/doc.rst', 'w') as f:
	for name, func in functions:
		if not name.startswith('_'):
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
