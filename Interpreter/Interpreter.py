from Interpreter.Number import *
from Interpreter.SymbolTable import *
from Lexer.Constants import *
from Lexer.Lexer import *
from Parser.Parser import *
from Runtime.Runtime import *

global_symbol_table = SymbolTable()

class Interpreter:
	"""docstring for Interpreter"""
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined')

	def visit_UseNode(self, node, context):
		res = RTResult()

		if node.status == "modl":
			if node.modl_name.value == "rand":
				global_symbol_table.set("rand", BuiltInFunction.rand)
				global_symbol_table.set("choice", BuiltInFunction.choice)

			elif node.modl_name.value == "isOBJ":
				global_symbol_table.set("isInt", BuiltInFunction.is_number)
				global_symbol_table.set("isStr", BuiltInFunction.is_string)
				global_symbol_table.set("isList", BuiltInFunction.is_list)
				global_symbol_table.set("isFunc", BuiltInFunction.is_function)

			elif node.modl_name.value == "Convert":
				global_symbol_table.set("ConStr", BuiltInFunction.constr)
				global_symbol_table.set("ConInt", BuiltInFunction.conint)

			elif node.modl_name.value == "time":
				global_symbol_table.set("sleep", BuiltInFunction.sleep)

			elif node.modl_name.value == "math":
				global_symbol_table.set("mathPi", Number.math_pi)
				global_symbol_table.set("mathE", Number.math_e)
				global_symbol_table.set("mathTau", Number.math_tau)


			else:
				return res.failrule(RTError(
					node.pos_start, node.pos_end,
					f"Module '{node.modl_name.value}' is not defined",
					context
				))
			return RTResult().success(
				String(node.modl_name.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		    )
		if node.status == "connect":
			fn1 = str(node.connect_name.value)
			fn = fn1

			allowed_extensions = ['.emr']
			try:
				with open(str(node.connect_name.value), 'r') as f:
					if BuiltInFunction.check_file_extension(self, str(node.connect_name.value), str(allowed_extensions)):
			 			script = f.read()
					else:
						return RTResult().failrule(RTError(
							node.pos_start, node.pos_end, f"Failed to load script \"{fn}\"\n" + "NOT .emr", context))
			except Exception as e:
				#if not  isinstance(list_, List):
				return RTResult().failrule(RTError(
					node.pos_start, node.pos_end, f"Failed to load script \"{fn}\"\n" + str(e), context))
			if script.strip() == "": pass
			else:
				_, error = Run.run(fn1, script)

				if error:
					return RTResult().failrule(RTError(
						node.pos_start,  node.pos_end, f"Failed to finish executing script \"{fn}\"\n" + error.as_string(), context))

			return RTResult().success(Number.null)


			return RTResult().success(
				String(node.connect_name.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		    )

	def visit_StringNode(self, node, context):
		return RTResult().success(
			String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
	    )

	def visit_NumberNode(self, node, context):
		return RTResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_ListNode(self, node, context):
		res = RTResult()
		elements = []

		for element_node in node.element_nodes:
			#print(element_node)
			elements.append(res.register(self.visit(element_node, context)))
			if res.should_return():
				return res

		return res.success(
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
		)

	def visit_str(self, node, context):
		res = RTResult()
		
		if node == 'pass':
			return res.success(Number.null)

	def visit_VarAccessNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failrule(RTError(
				node.pos_start, node.pos_end,
				f"'{var_name}' is not defined",
				context
		))
		value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RTResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.should_return(): return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RTResult()
		left = res.register(self.visit(node.left_node, context))
		if res.should_return(): return res
		right = res.register(self.visit(node.right_node, context))
		if res.should_return(): return res

		if node.op_tok.type == TOKEN_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TOKEN_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TOKEN_MUL:
			result, error = left.multed_by(right)
		elif node.op_tok.type == TOKEN_DIV:
			result, error = left.dived_by(right)
		elif node.op_tok.type == TOKEN_DIVA:
			result, error = left.diva_by(right)
		elif node.op_tok.type == TOKEN_REDIV:
			result, error = left.rediv_by(right)
		elif node.op_tok.type == TOKEN_POW:
			result, error = left.powed_by(right)
		elif node.op_tok.type == TOKEN_EE:
			result, error = left.get_comparison_eq(right)
		elif node.op_tok.type == TOKEN_NE:
			result, error = left.get_comparison_ne(right)
		elif node.op_tok.type == TOKEN_LT:
			result, error = left.get_comparison_lt(right)
		elif node.op_tok.type == TOKEN_GT:
			result, error = left.get_comparison_gt(right)
		elif node.op_tok.type == TOKEN_LTE:
			result, error = left.get_comparison_lte(right)
		elif node.op_tok.type == TOKEN_GTE:
			result, error = left.get_comparison_gte(right)

		elif node.op_tok.matches(TOKEN_KEYWORD, 'and'):
			result, error = left.anded_by(right)
		elif node.op_tok.matches(TOKEN_KEYWORD, 'or'):
		 	result, error = left.ored_by(right)
		elif node.op_tok.matches(TOKEN_KEYWORD, '!in'):
			result, error = left.not_in_by(right)
		elif node.op_tok.matches(TOKEN_KEYWORD, 'in'):
			result, error = left.in_by(right)

		#print(result)
		if error:
			return res.failrule(error)
		else:
			result = res.success(result.set_pos(node.pos_start, node.pos_end))
			return result

	def visit_IfNode(self, node, context):
		res = RTResult()

		for condition, expr, should_return_null in node.cases:
			#print(condition)
			condition_value = res.register(self.visit(condition, context))

			if res.should_return(): 
				return res

			if condition_value.is_true():
				expr_value = res.register(self.visit(expr, context))
				if res.should_return(): return res
				return res.success(Number.null if should_return_null else expr_value)

		if node.else_case:
			expr, should_return_null = node.else_case
			else_value = res.register(self.visit(expr, context))
			if res.should_return(): return res
			return res.success(Number.null if should_return_null else else_value)

		return res.success(Number.null)

	def visit_ForNode(self, node, context):
		res = RTResult()
		elements = []
		#print("popal")
		start_value = res.register(self.visit(node.start_value_node, context))
		if res.should_return(): return res

		end_value = res.register(self.visit(node.end_value_node, context))
		if res.should_return(): return res

		if node.step_value_node:
			step_value = res.register(self.visit(node.step_value_node, context))
			if res.should_return(): return res
		else:
			step_value = Number(1)

		i = start_value.value

		if isinstance(end_value, Number):
			if step_value.value >= 0:
				condition = lambda: i < end_value.value
			else:
				condition = lambda: i > end_value.value
				
			while condition():
				context.symbol_table.set(node.var_name_tok.value, Number(i))
				i += step_value.value

				value = res.register(self.visit(node.body_node, context))
				if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

				if res.loop_should_continue:
					continue 

				if res.loop_should_break:
					break

				elements.append(value)
			return res.success(Number.null if node.should_return_null else List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
		elif isinstance(end_value, List):

			try:
				if step_value.value >= 0:
					try:
						condition = lambda:  i < len(end_value.elements)
					except TypeError:
						return RTRessult().failrule(RTError(
							node.pos_start,  node.pos_end, f"the variable must be of numeric type, or there is another problem", context))

				else:
					condition = lambda: i > len(end_value.elements)
			except:
				return RTResult().failrule(RTError(
						node.pos_start,  node.pos_end, f"the variable must be of numeric type, or there is another problem", context))

			
			index = 0
			while condition():
				context.symbol_table.set(node.var_name_tok.value, end_value.elements[index])
				i += step_value.value

				value = res.register(self.visit(node.body_node, context))
				if res.should_return() and res.loop_should_continue == False and loop_should_break == False: return res

				if res.loop_should_continue:
					continue 

				if res.loop_should_break:
					break

				elements.append(value)
				index += 1
			return res.success(Number.null if node.should_return_null else List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
		elif isinstance(end_value, String):
			if step_value.value >= 0:
				condition = lambda: i < len(end_value.value)
			else:
				condition = lambda: i > len(end_value.value)
			
			index = 0
			while condition():
				context.symbol_table.set(node.var_name_tok.value, String(end_value.value[index]))
				i += step_value.value

				value = res.register(self.visit(node.body_node, context))
				if res.should_return() and res.loop_should_continue == False and loop_should_break == False: return res

				if res.loop_should_continue:
					continue 

				if res.loop_should_break:
					break

				elements.append(value)
				index += 1

			return res.success(Number.null if node.should_return_null else String(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

	def visit_TryNode(self, node, context):
		res = RTResult()
		elements = []

		value = res.register(self.visit(node.body_node, context))

		if res.error:
			new_condition = []
			add = False
			for nc in node.condition:
				if add == False:
					if nc.type == TOKEN_LPAREN:
						new_condition.append(nc)
						add = True
					else:
						new_condition.append(nc)
				if add == True:
					lexer = Lexer("<try>", '"'+res.error.as_string()+'"')
					tokens, error = lexer.make_tokens()
					
					new_condition.append(tokens[0])
					new_condition.append(Token(TOKEN_COMMA, pos_start=node.pos_start))
					add = False
			node.condition = new_condition
			parser = Parser(node.condition)
			context = Context('<try>')
			context.symbol_table = global_symbol_table
			ast = parser.parse()
			res = self.visit(ast.node, context)
			if res.error: return res
		#res.register(self.visit(node.body_node, context))

		return res.success(
			Number.null if node.should_return_null else 
			String("hi").set_context(context).set_pos(node.pos_start, node.pos_end)
	    )

	def visit_WhileNode(self, node, context):
		res = RTResult()
		elements = []

		while True: 
			condition = res.register(self.visit(node.condition_node, context))
			if res.should_return(): return res

			if not condition.is_true(): break

			value = res.register(self.visit(node.body_node, context))
			
			if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

			if res.loop_should_continue:
				continue 

			if res.loop_should_break:
				break

			elements.append(value)

		return res.success(
			Number.null if node.should_return_null else 
			List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
	    )

	def visit_UnaryOpNode(self, node, context):
		res = RTResult()
		number = res.register(self.visit(node.node, context))
		if res.should_return(): return res
		error = None

		if node.op_tok.type == TOKEN_MINUS:
			number, error = number.multed_by(Number(-1))
		elif node.op_tok.matches(TOKEN_KEYWORD, 'not'):
			number, error = number.notted()

		if error:
			return res.failrule(error)
		else:
			return res.success(number.set_pos(node.pos_start, node.pos_end))

	def visit_FuncDefNode(self, node, context):
		res = RTResult()

		func_name = node.var_name_tok.value if node.var_name_tok else None
		body_node = node.body_node
		arg_names = [arg_name.value for arg_name in node.arg_name_toks]
		func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

		if node.var_name_tok:
			context.symbol_table.set(func_name, func_value)

		if res.should_return(): return [], error
		return res.success(func_value)

	def visit_CallNode(self, node, context):
		res = RTResult()
		args = []

		value_to_call = res.register(self.visit(node.node_to_call, context))
		if res.should_return(): return res
		value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

		for arg_node in node.arg_nodes:
			args.append(res.register(self.visit(arg_node, context)))
			if res.error: return res

		return_value = res.register(value_to_call.execute(args))
		if res.should_return(): return res
		return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
		return res.success(return_value)

	def visit_ReturnNode(self, node, context):
		res = RTResult()

		if node.node_to_return:
			value = res.register(self.visit(node.node_to_return, context))
			if res.should_return(): return res
		else:
			value = Number.null
    
		return res.success_return(value)

	def visit_ContinueNode(self, node, context):
		return RTResult().success_continue()

	def visit_BreakNode(self, node, context):
		return RTResult().success_break()