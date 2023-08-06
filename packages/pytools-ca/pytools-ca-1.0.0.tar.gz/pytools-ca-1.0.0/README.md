# PyTools

Just a collection of useful tools.

## Features

* `nil`  & `null` ::

Shorthand values for for the `None` boolean value.

* `buildFunc(name='unnamed', param=[], func=['pass'], \*\*kwargs)` & `buildClass` ::

Functions that will build dynamically named and defined functions and classes respectively.
	
	buildFunc(
		name='a_function',
		param=[
			'value_1',
			'value_2'
		],
		func=[
			'a_variable = value_1 + value_2',
			'print(a_variable)'
		],
 		)

* `doLoggedAction(action='pass', log='Logged!', iterateMethod='set', logToScreen=True, logFile=None)` ::

Executes a block of code and logging it either on the screen or in a file.
Set `logToScreen` to False to only print to a file, and pass a path to a file as `logFile`
to log the code to the file.

	doLoggedAction(
		action='print(\'Hello World!\')',
		log='Printed!'
		)

	doLoggedAction('print(\'Hello World!\')', 'Printed!')

* clear() ::

Clears the screen regardless of what system is used.

	clear()

* `systemCheck(acceptedMachinesList=['Windows', 'Darwin', 'Linux'])` ::

Makes sure the machine the program is run on can properly run the program.

	systemCheck(['Windows', 'Linux'])

* `replaceLine(file, line, newText)` ::

Takes in a path to a file, the number of the line you want to change in the file, and the string you want to change it to.

	replaceLine('../text_files/a_file.txt', 3, 'This is a .txt file!')

* `lineBreakdown` ::

A class with multiple related functions in it.
	
	lineBreakdown().{METHOD}({PARAMETERS})

`length(origText, maxLength)` -

Takes a long string and breaks it down into a list of strings that conform to specified length requirements.

	lineBreakdown('Yesterday, I had work from 9:00 AM to 5:00 PM, and then I had to visit the grocery store.', 10) =>

	['Yesterday,', 'I had work', 'from 9:00', 'AM to 5:00', 'PM, and', 'then I had', 'to visit', 'the', 'grocery', 'store']

	lineBreakdown('Cardiovascular', 10) =>

	['Cardiovas-', 'cular']

`raw(line)` -

Removes the '\n' at the end of a string if it exists, this is meant for quickly iterating through a file.

	lineBreakdown().raw('Hello World!\n') =>

	'Hello World!'

	lineBreakdown().raw('Hello World!') =>

	'Hello World!'

`list(line)` -

Breaks down a line into a list of string that were previously joined by a '\n'.

	lineBreakdown().list('To-do List:\n- Water the plants.\n- Exercise.\n- Go to the grocery store for bread and milk.') =>

	['To-do List:', '- Water the plants.', '- Exercise.', '- Go to the grocery store for bread and milk.']

