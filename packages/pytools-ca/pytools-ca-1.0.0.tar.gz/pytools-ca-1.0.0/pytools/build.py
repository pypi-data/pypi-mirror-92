buildVar = lambda name, val=None: globals()[name] = val
def buildClass(name='unnamed', param=[], func=['pass'], **kwargs):
	if param != []:
		paramstr = param[0]
		del param[0]
		for i in param:
			paramstr = paramstr + ', ' + i
		paramstr = '(' + paramstr + '):'
	else:
		paramstr = ':'
	funcstr = ''
	for i in func:
		funcstr = funcstr + '\n\t' + i
	exec('class ' + name + paramstr + funcstr, globals())
def buildFunc(name='unnamed', param=[], func=['pass'], **kwargs):
	if param and param != [] and param != '' and param != ():
		paramstr = param[0]
		del param[0]
		for i in param:
			paramstr = paramstr + ', ' + i
	else:
		paramstr = ''
	funcstr = ''
	for i in func:
		funcstr = funcstr + '\n\t' + i
	exec('def ' + name + '(' + paramstr + '):' + funcstr, globals())