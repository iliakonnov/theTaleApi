#!/usr/bin/python
# coding:utf8
from theTaleApi import theTaleApi
import curses
import re
import inspect
import locale
from pprint import PrettyPrinter
import sys
reload(sys)
sys.setdefaultencoding('utf8')
locale.setlocale(locale.LC_ALL, "")


class UnicodePrettyPrinter(PrettyPrinter):
	"""Unicode-friendly PrettyPrinter
	Prints:
		- u'привет' instead of u'\u043f\u0440\u0438\u0432\u0435\u0442'
		- 'привет' instead of '\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'
	https://gist.github.com/shvechikov/1922650
	"""
	def format(self, *args, **kwargs):
		repr, readable, recursive = PrettyPrinter.format(self, *args, **kwargs)
		if repr:
			if repr[0] in ('"', "'"):
				repr = repr.decode('string_escape')
			elif repr[0:2] in ("u'", 'u"'):
				repr = repr.decode('unicode_escape').encode(sys.stdout.encoding)
		return repr, readable, recursive

	def _repr(self, object, context, level):
		repr, readable, recursive = self.format(object, context.copy(),
												self._depth, level)
		if not readable:
			self._readable = False
		if recursive:
			self._recursive = True
		return repr


def upprint(obj, stream=None, indent=1, width=180, depth=None):
	printer = UnicodePrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
	printer.pprint(obj)


def upformat(obj, stream=None, indent=1, width=180, depth=None):
	printer = UnicodePrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
	return printer.pformat(obj)


def classToDict(c):
	result = {}
	'''
	result = {
		"func1": {
			"desc": "Func1 description",
			"func": <func1 function object>,
			"params": {
				"param1": {
					"type": "str",
					"desc": "first param"
				},
				"param2": {
					"type": "int",
					"desc": "second param"
				}
			}
		},
		"func2": {
			"desc": "Func2 description",
			"func": <func2 function object>,
			"params": {
				"param1": {
					"type": "str",
					"desc": "first param"
				},
				"param2": {
					"type": "int",
					"desc": "second param"
				}
			}
		}
	}
	'''
	regexT = re.compile(':type (.+): (.+)')
	regexP = re.compile(':param (.+): (.+)')
	functions = inspect.getmembers(c, predicate=inspect.ismethod)
	allow = []
	for fName, func in functions:
		if not fName.startswith('_') or fName in allow:
			if fName not in result.keys():
				result[fName] = {'params': {}, 'func': func, 'desc': ''}
			for line in func.__doc__.split('\n'):
				l = line.replace('\t', '')
				if l.startswith(':param'):
					pName, pDesc = regexP.findall(l)[0]
					if pName not in result[fName]['params'].keys():
						result[fName]['params'][pName] = {'desc': '', 'type': ''}
					result[fName]['params'][pName]['desc'] = pDesc
				elif l.startswith(':type'):
					pName, pType = regexT.findall(l)[0]
					if pName not in result[fName]['params'].keys():
						result[fName]['params'][pName] = {'desc': '', 'type': ''}
					result[fName]['params'][pName]['type'] = pType
				elif not l.startswith(':') and not l.startswith('..') and bool(l):
					result[fName]['desc'] = l
	return result


def draw(screen, textKeys, textValues, selected, result):
	screen.erase()
	screen.addstr(0, 0, 'Press "q" to exit.', curses.A_UNDERLINE)
	for i in xrange(len(textKeys)):
		if i == selected:
			screen.addstr(i + 1, 0, textKeys[i], curses.A_REVERSE)
		else:
			screen.addstr(i + 1, 0, textKeys[i])
	screen.addstr(len(textKeys) + 1, 0, '=' * 9 + 'DESCRIPTION' + '=' * 10)
	screen.addstr(len(textKeys) + 2, 0, textValues[selected]['desc'])
	screen.addstr(len(textKeys) + 3, 0, '=' * 12 + 'INPUT' + '=' * 13)
	screen.addstr(len(textKeys) + 5, 0, '>')
	screen.addstr(len(textKeys) + 6, 0, '=' * 12 + 'RESULT' + '=' * 12)
	num = 0
	for line in str(result).split('\n'):
		screen.addstr(len(textKeys) + num + 7, 0, upformat(str(result)))
		num += 1
	screen.move(len(textKeys) + 5, 2)


def main(screen):
	api = theTaleApi('example-1')
	text = classToDict(api)
	textKeys = sorted(text.keys())
	textValues = []
	for i in textKeys:
		textValues.append(text[i])
	# print(textValues)
	selected = 0
	selecting = False
	result = ''
	'''
	Экран:
	Press "q" to exit.
	func1
	func2
	...
	==========  (+1)
	<описание>  (+2)
	==========  (+3)
	<вопрос>    (+4)
	<ввод>      (+5)
	=результат= (+6)
	<результат> (+7)
	'''
	while True:
		draw(screen, textKeys, textValues, selected, result)
		screen.refresh()
		key = screen.getch()
		if not selecting:
			if key == ord('q'):
				break
			elif key == curses.KEY_DOWN:
				if selected != len(textKeys) - 1:
					selected += 1
			elif key == curses.KEY_UP:
				if selected != 0:
					selected -= 1
			elif key == ord(' ') or key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
				selecting = True
				args = {}
				for key, value in textValues[selected]['params'].iteritems():
					draw(screen, textKeys, textValues, selected, result)
					screen.addstr(len(textKeys) + 4, 0, '{var} = {desc} ({type})'.format(
						var=key, desc=value['desc'], type=value['type']))
					screen.refresh()
					curses.echo()
					get = screen.getstr(len(textKeys) + 5, 2)
					if get:
						args[key] = get
					curses.noecho()
				try:
					result = textValues[selected]['func'](**args)
				except Exception as e:
					result = e.message
				selecting = False

curses.wrapper(main)
'''
main(None)'''
