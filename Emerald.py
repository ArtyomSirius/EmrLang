from Run.Run import *
from sys import argv

main = True
while main:
	try:
		text = f'run("{argv[1]}")'
		main = False
	except:
		main = False
		while True:
			print("Emerald (2023-2024) Version: 1.0")
			print("Введите 'help()' для справки")
			print("")
			text = input(">>> ")
			if text.strip() == "": continue
			result, error = run('<SHELL>',text)
			if error:
				print(error.as_string())
			elif result:
				if len(result.elements) == 1:
					print(repr(result.elements[0]))
				else:
					print(repr(result))
	print("Emerald (2023-2024) Version: 1.0")
	#print("Введите 'help()' для справки")
	print("")	
	if text.strip() == "": continue
	result, error = run('<SHELL>',text)
	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))
