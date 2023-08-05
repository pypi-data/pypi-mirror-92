
# Valtert 2020
# Last updated 22. december
# version 0.2
# License: MIT
version = 'version 0.8.2'


# --- lib ---
import os, sys
from inspect import getmembers, isfunction, isclass
from ._all_ import * #for initial test


# --- function ---
def _deleteSubfix(s):
	if s[-3:] == '.py':
		return s[:-3]
	else:
		return s


def _trimFolderList(l):

	if '.DS_Store' in l:
		l.pop(l.index('.DS_Store'))

	if '__init__.py' in l:
		l.pop(l.index('__init__.py'))

	if '__pycache__' in l:
		l.pop(l.index('__pycache__'))

	if '_all_.py' in l:
		l.pop(l.index('_all_.py'))


	return l


def _makeImportText(frm, imp, s, i):
	if len(s) == 0:
		return 'from .' + frm + ' import ' + imp + '\n'
	else:
		return 'from .' + s + '.' + frm + ' import ' + imp + '\n'


def _makeModulesFromFile(modules, s = '', i=''):

	modulesText = ''
	importText = ''

	exec('from .' + s +  ' import ' + modules)

	for func in getmembers(eval(modules), isfunction):
		modulesText += i + func[0] + ' = ' + func[0] + '\n'
		#importText += 'from .' + modules + ' import ' + func[0] + '\n'
		importText += _makeImportText(modules, func[0], s, i)


	for clss in getmembers(eval(modules), isclass):
		modulesText += i + clss[0] + ' = ' + clss[0] + '\n'
		#importText += 'from .' + modules + ' import ' + clss[0] + '\n'
		importText += _makeImportText(modules, clss[0], s, i)

	return modulesText, importText


def makeFile(version):
	
	path = __file__[:-11] + '_all_.py'
	file = open(path, 'w')
	file.write('')
	file.close()
	file = open(path, 'a')

	headFolder = _trimFolderList(os.listdir(__file__[:-11]))

	importText = ''
	modulesText = ''

	for sub in headFolder:
	
		if sub[-3:] == '.py':

			_0, _1 = _makeModulesFromFile(_deleteSubfix(sub))
			modulesText += _0
			importText += _1

		else:

			modulesText += 'class ' + _deleteSubfix(sub) + ':\n'
			for subsub in _trimFolderList(os.listdir(os.path.join(__file__[:-11], sub))):

				if subsub[-3:] == '.py':
					_0, _1 = _makeModulesFromFile(_deleteSubfix(subsub), sub, '    ')
					modulesText += _0
					importText +=  _1

	file.write('\n#AUTOMATED FILE\n#DO NOT EDIT\n#VALTERT\nVERSION = "' + version + '"\n')
	file.write('\n#--- Imports ---\n')
	file.write(importText)
	file.write('\n#--- Assigns ---\n')
	file.write(modulesText)

	file.close()


def test(v):
	
	try:
		if VERSION == v:
			return True
		else:
			return False

	except:
		return False


# --- import ---
if not test(version):
	makeFile(version)
	os.execl(sys.executable, sys.executable, *sys.argv)