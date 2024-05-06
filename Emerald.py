from Run.Run import *
from sys import argv

print("Emerald (2024)")
print("Версия: 0.9.9(Последний пре-релиз)")
print("Разработчик: Шелепнёв Артём")
print("Введите 'help()' для справки")
print("")




main = True
while main:
	try:
		text = f'run("{argv[1]}")'
		main = False
	except:
		main = False
		while True:
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
	if text.strip() == "": continue
	result, error = run('<SHELL>',text)
	if error:
		print(error.as_string())
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else:
			print(repr(result))
