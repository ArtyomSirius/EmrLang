from Errors.Errors import *
from Interpreter.SymbolTable import *
from Run import Run
from Interpreter import Interpreter
from random import randint
from random import choice
from random import shuffle
from Runtime.Runtime import *

import os
import math
import string

LETTERS          = string.ascii_letters

class ValueStr:
	def _ValueStr__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)

	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)

	def powed_by(self, other):
		return None, self.illegal_operation(other)

	def diva_by(self, other):
		return None, self.illegal_operation(other)		

	def rediv_by(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_ne(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)

	def anded_by(self, other):
		return None, self.illegal_operation(other)

	def ored_by(self, other):
		return None, self.illegal_operation(other)

	def notted(self):
		return None, self.illegal_operation(other)

	def execute(self, args):
		return RTResult().failrule(self.illegal_operation())

	def copy(self):
		raise Exception('No copy method defined')

	def in_by(self, args):
		return RTResult().failrule(self.illegal_operation())

	def not_in_by(self, args):
		return RTResult().failrule(self.illegal_operation())

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'Illegal operation',
			self.context
		)

		

class Value:
	def __init__(self):
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		return None, self.illegal_operation(other)

	def subbed_by(self, other):
		return None, self.illegal_operation(other)

	def multed_by(self, other):
		return None, self.illegal_operation(other)

	def dived_by(self, other):
		return None, self.illegal_operation(other)

	def powed_by(self, other):
		return None, self.illegal_operation(other)

	def diva_by(self, other):
		return None, self.illegal_operation(other)		

	def rediv_by(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_eq(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_ne(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gt(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_lte(self, other):
		return None, self.illegal_operation(other)

	def get_comparison_gte(self, other):
		return None, self.illegal_operation(other)

	def anded_by(self, other):
		return None, self.illegal_operation(other)

	def ored_by(self, other):
		return None, self.illegal_operation(other)

	def notted(self):
		return None, self.illegal_operation()

	def execute(self, args):
		return RTResult().failrule(self.illegal_operation())

	def string_not_int_index(self, args):
		return RTResult().failrule(self.string_not_int_index())

	def copy(self):
		raise Exception('No copy method defined')

	def is_true(self):
		return False

	def illegal_operation(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'Illegal operation',
			self.context
		)
	def string_not_int_index(self, other=None):
		if not other: other = self
		return RTError(
			self.pos_start, other.pos_end,
			'string index out of range',
			self.context
		)


class List(Value):
	def __init__(self, elements):
		super().__init__()
		self.elements = elements

	def added_to(self, other):
		new_list = self.copy()
		new_list.elements.append(other)
		return new_list, None

	def subbed_by(self, other):
		if isinstance(other, Number):
			new_list = self.copy()
			try:
				new_list.elements.pop(other.value)
				return new_list, None
			except:
				return None, RTError(
					other.pos_start, other.pos_end, 'Element at this index could not be removed from list because index is out of bounds',
					self.context
				)

		else:
			return None, Value.illegal_operation(self, other)


	def multed_by(self, other):
		if isinstance(other, List):
			new_list = self.copy()
			new_list.elements.extend(other.elements)
			return new_list, None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			try:
				return self.elements[other.value], None
			except:
				return None, RTError(
					other.pos_start, other.pos_end, 'Element at this index could not be retrivied from list because index is out of bounds',
					self.context
				)

		else:
			return None, Value.illegal_operation(self, other)

	def in_by(self, other):
		if isinstance(other, List):
			return Number(int(self.value in other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def copy(self):
		copy = List(self.elements)
		copy.set_context(self.set_context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __str__(self):
		return ", ".join([str(x) for x in self.elements])

	def __repr__(self):
		return f'[{", ".join([str(x) for x in self.elements])}]'


class Number(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def set_context(self, context=None):
		self.context = context
		return self
	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end, 'Division by zero',
					self.context
				)
			return Number(self.value / other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def diva_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end, 'Division by zero',
					self.context
				)
			return Number(self.value // other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_eq(self, other):
		if isinstance(other, Number):	
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, Number):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, Number):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, Number):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, Number):
			return Number(int(int(self.value) and int(other.value))).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def in_by(self, other):
		if isinstance(other, Number):
			return Number(int(int(self.value) in int(other.value))).set_context(self.context), None
		elif isinstance(other, List):
			return Number(int(str(self.value) in str(other.elements))).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def not_in_by(self, other):
		if isinstance(other, Number):
			return Number(int(int(self.value) not in int(other.value))).set_context(self.context), None
		elif isinstance(other, List):
			return Number(int(str(self.value) not in str(other.elements))).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def ored_by(self, other):
		if isinstance(other, Number):
			return Number(int(int(self.value) or int(other.value))).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def notted(self):
		return Number(1 if self.value == 0 else 0).set_context(self.context), None


	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.pos_start, self.pos_end)
		copy.set_context(self.context)
		return copy

	def is_true(self):
		return self.value != 0

	def rediv_by(self, other):
		if isinstance(other, Number):
			return Number(self.value % other.value).set_context(self.context), None

	def __repr__(self):
		return str(self.value)

class String(Value):
	def __init__(self, value):
		super().__init__()
		self.value = value

	def added_to(self, other):
		if isinstance(other, String):
			return String(self.value + other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def multed_by(self, other):
		if isinstance(other, Number):
			return String(self.value * other.value).set_context(self.context), None
		else:
			return None, Value.illegal_operation(self, other)

	def dived_by(self, other):
		if isinstance(other, Number):
			try:
				return String(self.value[other.value]).set_context(self.context), None
			except IndexError:
				return None,  Value.string_not_int_index(self, other)
		else:
			return None, Value.illegal_operation(self, other)

	def is_true(self):
		return len(self.value) > 0

	def __str__(self):
		return self.value

	def copy(self):
		copy = String(self.value)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def get_comparison_eq(self, other):
		if isinstance(other, String):
			#result = Number(int(self.value == other.value)).set_context(self.context), None
			return Number(int(self.value == other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def get_comparison_ne(self, other):
		if isinstance(other, String):
			return Number(int(self.value != other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def get_comparison_lt(self, other):
		if isinstance(other, String):
			return Number(int(self.value < other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def get_comparison_gt(self, other):
		if isinstance(other, String):
			return Number(int(self.value > other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def get_comparison_lte(self, other):
		if isinstance(other, String):
			return Number(int(self.value <= other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def get_comparison_gte(self, other):
		if isinstance(other, String):
			return Number(int(self.value >= other.value)).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def anded_by(self, other):
		if isinstance(other, String):
			return Number(int(str(self.value) and str(other.value))).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def in_by(self, other):
		if isinstance(other, String):
			return Number(int(str(self.value) in str(other.value))).set_context(self.context), None
		elif isinstance(other, List):
			return Number(int(str(self.value) in str(other.elements))).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def not_in_by(self, other):
		if isinstance(other, String):
			return Number(int(str(self.value) not in str(other.value))).set_context(self.context), None
		elif isinstance(other, List):
			return Number(int(str(self.value) not in str(other.elements))).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)


	def ored_by(self, other):
		if isinstance(other, String):
			return Number(int(str(self.value) or str(other.value))).set_context(self.context), None
		else:
			return None, ValueStr.illegal_operation(self, other)

	def __repr__(self):
		return f'"{self.value}"'

class BaseFunction(Value):
	def __init__(self, name):
		super().__init__()
		self.name = name or "<anonymous>"

	def generate_new_context(self):
		new_context = Context(self.name, self.context, self.pos_start)
		new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
		return new_context

	def check_args(self, arg_names, args):
		res = RTResult()

		if len(args) > len(arg_names):
			return res.failrule(RTError(
				self.pos_start, self.pos_end,
				f"{len(args) - len(arg_names)} too many args passed into '{self.name}'",
				self.context
			))
		
		if len(args) < len(arg_names):
			return res.failrule(RTError(
				self.pos_start, self.pos_end,
				f"{len(arg_names) - len(args)} too few args passed into '{self.name}'",
				self.context
			))

		return res.success(None)

	def populate_args(self, arg_names, args, exec_ctx):
		for i in range(len(args)):
			arg_name = arg_names[i]
			arg_value = args[i]
			arg_value.set_context(exec_ctx)
			exec_ctx.symbol_table.set(arg_name, arg_value)

	def check_and_populate_args(self, arg_names, args, exec_ctx):
		res = RTResult()
		res.register(self.check_args(arg_names, args))
		if res.should_return(): return res
		self.populate_args(arg_names, args, exec_ctx)
		return res.success(None)

class Function(BaseFunction):
	def __init__(self, name, body_node, arg_names, should_auto_return):
		super().__init__(name)
		self.body_node = body_node
		self.arg_names = arg_names
		self.should_auto_return = should_auto_return

	def execute(self, args):
		res = RTResult()  
		interpreter = Interpreter.Interpreter()
		exec_ctx = self.generate_new_context()
		
		res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
		if res.should_return(): return res

		value = res.register(interpreter.visit(self.body_node, exec_ctx))
		if res.should_return() and res.func_return_value == None: return res
		
		res_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
		return res.success(res_value)

	def copy(self):
		copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
	def __init__(self, name):
		super().__init__(name)

	def execute(self, args):
		res = RTResult()
		exec_ctx = self.generate_new_context()

		method_name = f'execute_{self.name}'
		method = getattr(self, method_name, self.no_visit_method)

		res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
		if res.should_return(): return res

		return_value = res.register(method(exec_ctx))
		if res.should_return(): return res
		return res.success(return_value)

	def no_visit_method(self, node, context):
		raise Exception(f"No execute_{self.name} method defined")

	def copy(self):
		copy = BuiltInFunction(self.name)
		copy.set_context(self.context)
		copy.set_pos(self.pos_start, self.pos_end)
		return copy

	def __repr__(self):
		return f"<built-in in function {self.name}>"

	def execute_print(self, exec_ctx):
		try:
			print(str(exec_ctx.symbol_table.get('value')))
		except TypeError:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "This type cannot be displayed in the console", exec_ctx))
		return RTResult().success(Number.null)
	execute_print.arg_names = ["value"]

	def execute_print_ret(self, exec_ctx):
		return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
	execute_print_ret.arg_names = ["value"]


	def execute_input(self, exec_ctx):
		message = exec_ctx.symbol_table.get("message")
		if not  isinstance(message, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be string!", exec_ctx))
		text = input(message)
		return RTResult().success(String(text))
	execute_input.arg_names = ["message"]

	def execute_input_int(self, exec_ctx):
		message = exec_ctx.symbol_table.get("message")
		if not  isinstance(message, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be string!", exec_ctx))
		while True:
			text = input(message)
			try:
				number = int(text)
				break
			except ValueError:
				print(f"'{text}' must be an integer. Try again")
		return RTResult().success(Number(number))
	execute_input_int.arg_names = ["message"]

	def execute_write(self, exec_ctx):
		file_ = exec_ctx.symbol_table.get('file')
		data_ = exec_ctx.symbol_table.get('data')
		if not isinstance(data_, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Second argument must be string!", exec_ctx))
		print(file_.value)
		file_.value.write(data_.value)


	execute_write.arg_names = ['file', 'data']
	def execute_clear(self, exec_ctx):
		os.system('cls' if os.name == 'nt' else "clear")
		return RTResult().success(Number.null)
	execute_clear.arg_names = []

	def execute_is_number(self, exec_ctx):
		is_number = isinstance(exec_ctx.symbol_table.get('value'), Number)
		return RTResult().success(Number.true if is_number else Number.false)
	execute_is_number.arg_names = ['value']

	def execute_is_string(self, exec_ctx):
		is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
		return RTResult().success(Number.true if is_string else Number.false)
	execute_is_string.arg_names = ["value"]

	def execute_is_list(self, exec_ctx):
		is_list = isinstance(exec_ctx.symbol_table.get('value'), List)
		return RTResult().success(Number.true if is_list else Number.false)
	execute_is_list.arg_names = ['value']

	def execute_is_function(self, exec_ctx):
		is_function = isinstance(exec_ctx.symbol_table.get('value'), BaseFunction)
		return RTResult().success(Number.true if is_function else Number.false)
	execute_is_function.arg_names = ['value']

	def execute_append(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get('list')
		value = exec_ctx.symbol_table.get('value')
		if not  isinstance(list_, List):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "First argument must be list!", exec_ctx))
		list_.elements.append(value)
		return RTResult().success(Number.null)
	execute_append.arg_names = ['list', 'value']

	def execute_pop(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get('list')
		value = exec_ctx.symbol_table.get('value')

		if not  isinstance(list_, List):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "First argument must be list!", exec_ctx))

		if not  isinstance(list_, Number):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Second argument must be number!", exec_ctx))

		try:
			elements = list_.elements.pop(index.value)
		except:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Element at this index could not be removed from list because index is out of bounds", exec_ctx))

		return RTResult().success(elements)
	execute_pop.arg_names = ['list', 'index']

	def execute_rand(self, exec_ctx):
		value1 = exec_ctx.symbol_table.get('value1')
		value2 = exec_ctx.symbol_table.get('value2')
		
		if not  isinstance(value1, Number):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "First argument must be number!", exec_ctx))

		if not  isinstance(value2, Number):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Second argument must be number!", exec_ctx))
			
		expression = f"randint({value1}, {value2})"
		result = eval(expression)
		return RTResult().success(Number(result))

	execute_rand.arg_names = ['value1', 'value2']

	def execute_choice(self, exec_ctx):
		value1 = exec_ctx.symbol_table.get('value1')
		if isinstance(value1, List):
			expression = f"choice({value1.elements})"
			result = eval(expression)
			return RTResult().success(String(result))
		elif isinstance(value1, String):
			expression = f'choice("{value1.value}")'
			result = eval(expression)
			return RTResult().success(String(result))
		else:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be string or list", exec_ctx))


	execute_choice.arg_names = ['value1']


	def execute_extend(self, exec_ctx):
		listA = exec_ctx.symbol_table.get('listA')
		listB = exec_ctx.symbol_table.get('listB')

		if not  isinstance(list_, List):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "First argument must be list!", exec_ctx))

		if not  isinstance(list_, List):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Second argument must be list!", exec_ctx))

		listA.elements.extend(listB.elements)
		return RTResult().success(Number.null)

	execute_extend.arg_names = ['listA', 'listB']

	def execute_quit(self, exec_ctx):
		quit()

	execute_quit.arg_names = []

	def execute_constr(self, exec_ctx):
		object_ = exec_ctx.symbol_table.get("object")
		#print(object_)

		if not isinstance(object_, Number) and not isinstance(object_, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be number or string!", exec_ctx))

		try:
			return RTResult().success(String(str(object_.value)))
		except:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, f"The '{object_}' cannot be converted to a string!", exec_ctx))

	execute_constr.arg_names = ["object"]

	def execute_conint(self, exec_ctx):
		object_ = exec_ctx.symbol_table.get("object")
		#print(object_)

		if not isinstance(object_, Number) and not isinstance(object_, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be number or string!", exec_ctx))

		try:
			return RTResult().success(Number(int(object_.value)))
		except:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, f"The '{object_}' cannot be converted to a number!", exec_ctx))

	execute_conint.arg_names = ["object"]

	def execute_help(self, exec_ctx):
		print("")
		print("Emerald - язык програмированния, созданный в качестве эксперимента.")
		print("	run(<you_file>) - запускает внешний файл(<you_file> замените на путь к вашему файлу) ")
		print("		Файл должен быть с расширением .emr!")
		print("В релизе тут будет больше информации))")

		return RTResult().success(Number(0))

	execute_help.arg_names = []

	def execute_Rstrip(self, exec_ctx):
		object_ = exec_ctx.symbol_table.get("string")
		if not isinstance(object_, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be number or string!", exec_ctx))
		return RTResult().success(String(object_.value.rstrip()))

	execute_Rstrip.arg_names = ['string']

	def execute_Lstrip(self, exec_ctx):
		object_ = exec_ctx.symbol_table.get("string")
		if not isinstance(object_, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be number or string!", exec_ctx))
		return RTResult().success(String(object_.value.lstrip()))

	execute_Lstrip.arg_names = ['string']

	def execute_sleep(self, exec_ctx):
		time = exec_ctx.symbol_table.get("time")
		if not isinstance(time, Number):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be number!", exec_ctx))
		from time import sleep
		sleep(int(time.value))
		return RTResult().success(Number(0))

	execute_sleep.arg_names = ["time"]

	def execute_open_file(self, exec_ctx):
		file = exec_ctx.symbol_table.get("file")
		parametr = exec_ctx.symbol_table.get("parametr")

		if isinstance(file, Number):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "First argument must be string!", exec_ctx))

		if not isinstance(parametr, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Second argument must be string!", exec_ctx))

		if parametr.value == "r":
			try:
				try:
					file = open(file.value, 'r').read()
					return RTResult().success(String(file))
				finally:
					file.close()
			except:
				return RTResult().failrule(RTError(
					self.pos_start, self.pos_end, f"File {file.value} is not defined", exec_ctx))
		elif parametr.value == "rl":
			try:
				try:
					file =  open(file.value, 'r').readlines()
					list_ = []
					for line in file:
						line = String(line)
						list_.append(line)
					return RTResult().success(List(list_))
				finally:
					file.close()
			except:
				return RTResult().failrule(RTError(
					self.pos_start, self.pos_end, f"File {file} is not defined", exec_ctx))
		elif parametr.value == "w":
			try:
				try:
					file_1 =  open(file.value, 'w')
					file_2 = file_1
					#file.write(str(exec_ctx.symbol_table.get("value")))
					return RTResult().success(String(file_2))
				finally:
					pass
					#file_1.close()
					#return RTResult().success(String(file_2))

				#return RTResult().success(List(list_))

			except ValueError as a:
				return RTResult().failrule(RTError(
					self.pos_start, self.pos_end, f"{a}", exec_ctx))


		else:
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, f"The 'open' function has no parameter {parametr}!", exec_ctx))


	execute_open_file.arg_names = ['file', 'parametr']

	def execute_len(self, exec_ctx):
		list_ = exec_ctx.symbol_table.get("list")
		if isinstance(list_, String):
			return RTResult().success(Number(len(list_.value)))
		elif isinstance(list_, List):
			return RTResult().success(Number(len(list_.elements)))
		else:
			#if not isinstance(list_, List):
		 	return RTResult().failrule(RTError(
		 		self.pos_start, self.pos_end,
		 		"Argument must be list or string",
		 		exec_ctx
		 	))
	execute_len.arg_names = ["list"]

	def execute_tracebackerr(self, exec_ctx):
		message = exec_ctx.symbol_table.get("message")
		if isinstance(message, String):
			return RTResult().failrule(RTError(
		 		self.pos_start, self.pos_end,
		 		message,
		 		exec_ctx
		 	))
		else:
			return RTResult().failrule(RTError(
		 		self.pos_start, self.pos_end,
		 		"Argument must be string!",
		 		exec_ctx
		 	))

	execute_tracebackerr.arg_names = ["message"]


	def check_file_extension(self, file_path, allowed_extensions):
			_, file_extension = os.path.splitext(file_path)
			file_extension = file_extension.lower()  # Преобразование расширения в нижний регистр
			return file_extension in allowed_extensions

	def execute_run(self, exec_ctx):
		fn = exec_ctx.symbol_table.get("fn")
		if not  isinstance(fn, String):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, "Argument must be string!", exec_ctx))
		fn = fn.value

		allowed_extensions = ['.emr']
		try:
			with open(fn, 'r') as f:
				if self.check_file_extension(fn, allowed_extensions):
		 			script = f.read()
				else:
					return RTResult().failrule(RTError(
						self.pos_start, self.pos_end, f"Failed to load script \"{fn}\"\n" + "NOT .emr", exec_ctx))
		except Exception as e:
			#if not  isinstance(list_, List):
			return RTResult().failrule(RTError(
				self.pos_start, self.pos_end, f"Failed to load script \"{fn}\"\n" + str(e), exec_ctx))
		if script.strip() == "": pass
		else:
			_, error = Run.run(fn, script)

			if error:
				return RTResult().failrule(RTError(
					self.pos_start, self.pos_end, f"Failed to finish executing script \"{fn}\"\n" + error.as_string(), exec_ctx))

		return RTResult().success(Number.null)

	execute_run.arg_names = ['fn']

BuiltInFunction.print        = BuiltInFunction("print")
BuiltInFunction.print_ret    = BuiltInFunction("print_ret")
BuiltInFunction.input        = BuiltInFunction("input")
BuiltInFunction.input_int    = BuiltInFunction("input_int")
BuiltInFunction.clear        = BuiltInFunction("clear")
BuiltInFunction.is_number    = BuiltInFunction("is_number")
BuiltInFunction.is_string    = BuiltInFunction("is_string")
BuiltInFunction.is_list      = BuiltInFunction("is_list")
BuiltInFunction.is_function  = BuiltInFunction("is_function")
BuiltInFunction.append       = BuiltInFunction("append")
BuiltInFunction.pop          = BuiltInFunction("pop")
BuiltInFunction.extend       = BuiltInFunction("extend")

BuiltInFunction.rand         = BuiltInFunction("rand")
BuiltInFunction.choice       = BuiltInFunction("choice")
BuiltInFunction.shuffle      = BuiltInFunction("shuffle")

BuiltInFunction.Lstrip       = BuiltInFunction("Lstrip")
BuiltInFunction.Rstrip       = BuiltInFunction("Rstrip")

BuiltInFunction.constr       = BuiltInFunction("constr")
BuiltInFunction.conint       = BuiltInFunction("conint")

BuiltInFunction.open_file    = BuiltInFunction("open_file")
BuiltInFunction.write        = BuiltInFunction("write")

BuiltInFunction.tracebackerr = BuiltInFunction("tracebackerr")

BuiltInFunction.sleep        = BuiltInFunction("sleep")

BuiltInFunction.len	         = BuiltInFunction("len")
BuiltInFunction.quit         = BuiltInFunction("quit")
BuiltInFunction.help         = BuiltInFunction("help")
BuiltInFunction.run          = BuiltInFunction("run")

Number.null     = Number(0)
Number.false    = Number(0)
Number.true     = Number(1)
Number.math_pi  = Number(math.pi)
Number.math_e   = Number(math.e)
Number.math_tau = Number(math.tau)