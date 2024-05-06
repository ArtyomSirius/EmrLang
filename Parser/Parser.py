from Parser.Nodes.NumberNode import *
from Parser.Nodes.BinOpNode import *
from Parser.Nodes.UnaryOpNode import *
from Parser.Nodes.VarAccessNode import *
from Parser.Nodes.VarAssignNode import *
from Parser.Nodes.IfNode import *
from Parser.Nodes.ForNode import *
from Parser.Nodes.WhileNode import *
from Parser.Nodes.FuncDefNode import *
from Parser.Nodes.CallNode import *
from Parser.Nodes.StringNode import *
from Parser.Nodes.ListNode import *
from Parser.Nodes.UseNode import *
from Parser.Nodes.BreakNode import *
from Parser.Nodes.ContinueNode import *
from Parser.Nodes.ReturnNode import *
from Parser.Nodes.TryNode import *
from Errors.Errors import *
from Lexer.Constants import *
from Lexer.Token import *

class Parser:
	"""docstring for Parser"""
	def __init__(self, tokens):
		self.tokens = tokens
		#print(tokens)
		self.tok_idx = -1
		self.advance()

	def reverse(self, amount=1):
		self.tok_idx -= amount
		self.update_current_tok()
		return self.current_tok

	def update_current_tok(self):
		if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx]


	def advance(self):
		self.tok_idx += 1
		self.update_current_tok()
		return self.current_tok

	def statements(self):
		res = ParseResult()
		statements = []
		pos_start = self.current_tok.pos_start.copy()

		while self.current_tok.type == TOKEN_NEWLINE:
			res.register_advancement()
			self.advance()

		statement = res.register(self.statement())
		if res.error: return res
		statements.append(statement)

		more_statements = True

		while True:
			newline_count = 0
			while self.current_tok.type == TOKEN_NEWLINE:
				res.register_advancement()
				self.advance()			
				newline_count += 1

			if newline_count == 0:
				more_statements = False

			if not more_statements: break
			statement = res.try_register(self.statement())
			if not statement:
				self.reverse(res.to_reverce_count)
				more_statements = False
				continue
			statements.append(statement)

		return res.success(ListNode(statements, pos_start, self.current_tok.pos_end.copy()))

	def statement(self):
		res = ParseResult()
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.matches(TOKEN_KEYWORD, 'return'):
			res.register_advancement()
			self.advance()

			expr = res.try_register(self.expr())
			if not expr:
				self.reverse(res.to_reverse_count)
			return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TOKEN_KEYWORD, "continue"):
			res.register_advancement()
			self.advance()

			return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

		if self.current_tok.matches(TOKEN_KEYWORD, "break"):
			res.register_advancement()
			self.advance()

			return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))
		expr = res.register(self.expr())
		if res.error: return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'return', 'continue', 'break', var', int, float, identifier, '+', '-' or '('"))
		return res.success(expr)

	def parse(self):
		res = self.statements()
		if not res.error and self.current_tok.type != TOKEN_EOF:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Token cannot appear after previous tokens"
			))
		return res

	def class_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TOKEN_KEYWORD, 'class'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'class'"
			))
	def for_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TOKEN_KEYWORD, 'for'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'for'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TOKEN_IDENTIFIER:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected identifier"
			))

		var_name = self.current_tok
		res.register_advancement()
		self.advance()


		if self.current_tok.type != TOKEN_EQ:
			res.register_advancement()
			self.advance()
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '='"
			))

		res.register_advancement()
		self.advance()

		start_value = res.register(self.expr())
		if res.error: return res

		if not self.current_tok.matches(TOKEN_KEYWORD, 'to'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'to'"
			))
			
		res.register_advancement()
		self.advance()

		end_value = res.register(self.expr())
		if res.error: return res

		if self.current_tok.matches(TOKEN_KEYWORD, 'step'):
			res.register_advancement()
			self.advance()

			step_value = res.register(self.expr())
			if res.error: return res
		else:
			step_value = None

		if not self.current_tok.matches(TOKEN_KEYWORD, '{'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()


		if self.current_tok.type == TOKEN_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: return res

			if not self.current_tok.matches(TOKEN_KEYWORD, '}'):
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))

			res.register_advancement()
			self.advance()

			return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
    
		body = res.register(self.statement())
		if res.error: return res

		return res.success(WhileNode(condition, body, False))

	def while_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TOKEN_KEYWORD, 'while'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'while'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: 
			return res

		if not self.current_tok.matches(TOKEN_KEYWORD, '{'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()
		if self.current_tok.type == TOKEN_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: 
				return res

			#print(f"a {self.current_tok}")

			if not self.current_tok.matches(TOKEN_KEYWORD, '}'):
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))

			#print("df")

			res.register_advancement()
			self.advance()

			return res.success(WhileNode(condition, body, True))
    
		body = res.register(self.statement())
		if res.error: 
			return res

		return res.success(WhileNode(condition, body, False))

	def try_expr(self):
		res = ParseResult()

		if not self.current_tok.matches(TOKEN_KEYWORD, 'try'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'try'"
			))

		res.register_advancement()
		self.advance()
		if res.error: 
			return res

		#print(self.current_tok.type)
		if self.current_tok.type != TOKEN_LPAREN:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '('"
			))
		lparen = self.current_tok
		res.register_advancement()
		self.advance()

		if self.current_tok.type != TOKEN_IDENTIFIER:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'identifier'"
			))

		identifier = self.current_tok
		condition = []
		condition.append(self.current_tok)
		condition.append(lparen)
		res.register_advancement()
		self.advance()
		
		if self.current_tok.type != TOKEN_LPAREN:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '('"
			))

		while True:
			res.register_advancement()
			self.advance()
			
			condition.append(self.current_tok)

			if self.current_tok.type == TOKEN_RPAREN:
				break
		

		res.register_advancement()
		self.advance()

		if self.current_tok.type != TOKEN_RPAREN:
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected ')'"
			))

		res.register_advancement()
		self.advance()


		if not self.current_tok.matches(TOKEN_KEYWORD, '{'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '{'"
			))

		res.register_advancement()
		self.advance()
		if self.current_tok.type == TOKEN_NEWLINE:
			res.register_advancement()
			self.advance()

			body = res.register(self.statements())
			if res.error: 
				return res

			#print(f"a {self.current_tok}")

			if not self.current_tok.matches(TOKEN_KEYWORD, '}'):
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected '}'"
				))

			#print("df")

			res.register_advancement()
			self.advance()

			return res.success(TryNode(identifier, condition, body, True))
    
		body = res.register(self.statement())
		if res.error: 
			return res

		return res.register(TryNode(identifier, condition, body, False))


	def if_expr(self):
		res = ParseResult()
		all_cases = res.register(self.if_expr_cases('if'))
		if res.error: return res
		cases, else_case = all_cases
		return res.success(IfNode(cases, else_case))

	def if_expr_b(self):
		return self.if_expr_cases('elif')

	def if_expr_c(self):
		res = ParseResult()
		else_case = None

		if self.current_tok.matches(TOKEN_KEYWORD, 'else'):
			res.register_advancement()
			self.advance()

			if self.current_tok.matches(TOKEN_KEYWORD, "{"):
				res.register_advancement()
				self.advance()

				statements = res.register(self.statements())
				if res.error: return res
				else_case = (statements, True)

				if self.current_tok.matches(TOKEN_KEYWORD, '}'):
					res.register_advancement()
					self.advance()
				else:
					return res.failrule(IllegalSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
							"Expected '}'"
					))
			else:
				expr = res.register(self.statement())
				if res.error: return res
				else_case = (expr, False)

		return res.success(else_case)

	def if_expr_b_or_c(self):
		res = ParseResult()
		cases, else_case = [], None

		if self.current_tok.matches(TOKEN_KEYWORD, 'elif'):
			all_cases = res.register(self.if_expr_b())
			if res.error: return res
			cases, else_case = all_cases
		else:
			else_case = res.register(self.if_expr_c())
			if res.error: return res

		return res.success((cases, else_case))

	def if_expr_cases(self, case_keyword):
		res = ParseResult()
		cases = []
		else_case = None

		if not self.current_tok.matches(TOKEN_KEYWORD, case_keyword):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '{case_keyword}'"
			))

		res.register_advancement()
		self.advance()

		condition = res.register(self.expr())
		if res.error: return res

		if not self.current_tok.matches(TOKEN_KEYWORD, '{'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"An extra identIfier/token is present or the '{' token is missing"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TOKEN_NEWLINE:
			res.register_advancement()
			self.advance()

			statements = res.register(self.statements())
			if res.error: return res
			cases.append((condition, statements, True))

			if self.current_tok.matches(TOKEN_KEYWORD, '}'):
				res.register_advancement()
				self.advance()
			else:
				all_cases = res.register(self.if_expr_b_or_c())
				if res.error: return res
				new_cases, else_case = all_cases
				cases.extend(new_cases)
		else:
			expr = res.register(self.statement())
			if res.error: return res
			cases.append((condition, expr, False))

			all_cases = res.register(self.if_expr_b_or_c())
			if res.error: return res
			new_cases, else_case = all_cases
			cases.extend(new_cases)

		return res.success((cases, else_case))

	def call(self):
		res = ParseResult()
		atom = res.register(self.atom())
		if res.error: return res

		if self.current_tok.type == TOKEN_LPAREN:
			res.register_advancement()
			self.advance()
			arg_nodes = []

			if self.current_tok.type == TOKEN_RPAREN:
				res.register_advancement()
				self.advance()
			else:
				arg_nodes.append(res.register(self.expr()))
				if res.error:
						return res.failrule(IllegalSyntaxError(
							self.current_tok.pos_start, self.current_tok.pos_end,
							"Expected ')', 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(' or 'not'"
						))
				while self.current_tok.type == TOKEN_COMMA:
					res.register_advancement()
					self.advance()

					arg_nodes.append(res.register(self.expr()))
					if res.error: return res

				if self.current_tok.type != TOKEN_RPAREN:
					return res.failrule(IllegalSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected ',' or ')'"
					))

				res.register_advancement()
				self.advance()
			return res.success(CallNode(atom, arg_nodes))
		return res.success(atom)
		
	def atom(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TOKEN_INT, TOKEN_FLOAT):
			res.register_advancement()
			self.advance()
			return res.success(NumberNode(tok))

		elif tok.type == TOKEN_STRING:
			res.register_advancement()
			self.advance()
			return res.success(StringNode(tok))

		elif tok.type == TOKEN_LSQUARE:
			list_expr = res.register(self.list_expr())
			if res.error: return res
			return res.success(list_expr)

		elif tok.type == TOKEN_IDENTIFIER:
			res.register_advancement()
			self.advance()
			return res.success(VarAccessNode(tok))

		elif tok.type == TOKEN_LPAREN:
			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res

			if self.current_tok.type == TOKEN_RPAREN:
				res.register_advancement()
				self.advance()
				return res.success(expr)
			else:
				return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))

		elif tok.matches(TOKEN_KEYWORD, 'for'):
			for_expr = res.register(self.for_expr())
			if res.error: return res
			return res.success(for_expr)

		elif tok.matches(TOKEN_KEYWORD, 'while'):
			while_expr = res.register(self.while_expr())
			if res.error: return res
			return res.success(while_expr)

		elif tok.matches(TOKEN_KEYWORD, 'func'):
			func_expr = res.register(self.func_def())
			if res.error: return res
			return res.success(func_expr)

		elif tok.matches(TOKEN_KEYWORD, 'class'):
			class_expr = res.register(self.class_def())
			if res.error: return res
			return res.success(class_expr)

		elif tok.matches(TOKEN_KEYWORD, 'if'):
			if_expr = res.register(self.if_expr())
			if res.error: return res
			return res.success(if_expr)

		elif tok.matches(TOKEN_KEYWORD, 'try'):
			try_expr = res.register(self.try_expr())
			if res.error: return res
			return res.success(try_expr)

		return res.failrule(IllegalSyntaxError(tok.pos_start, tok.pos_end, "Expected int, float, identifier, '+', '-' or '('"))

	def power(self):
		return self.bin_op(self.call, (TOKEN_POW, ), self.factor)
	def rediv(self):
		return self.bin_op(self.atom, (TOKEN_REDIV, ), self.factor)

	def list_expr(self):
		res = ParseResult()
		element_nodes = []
		pos_start = self.current_tok.pos_start.copy()

		if self.current_tok.type != TOKEN_LSQUARE:
			#if not self.current_tok.matches(TOKEN_KEYWORD, 'func'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected '['"
			))			

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TOKEN_RSQUARE:
			res.register_advancement()
			self.advance()
		else:
			element_nodes.append(res.register(self.expr()))
			if res.error:
					return res.failure(IllegalSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						"Expected '], 'var', 'if', 'for', 'while', 'func', int, float, identifier, '+', '-', '(', '[' or 'not'"
					))
			while self.current_tok.type == TOKEN_COMMA:
				res.register_advancement()
				self.advance()

				element_nodes.append(res.register(self.expr()))
				if res.error: return res

			if self.current_tok.type != TOKEN_RSQUARE:
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected ',' or ']'"
				))

			res.register_advancement()
			self.advance()

		return res.success(ListNode(
			element_nodes,
			pos_start,
			self.current_tok.pos_end.copy()
		))


	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TOKEN_PLUS, TOKEN_MINUS):
			res.register_advancement()
			self.advance()
			factor = res.register(self.factor())
			if res.error:
				return res
			return res.success(UnaryOpNode(tok, factor))


		return self.power()

	def comp_expr(self):
		res = ParseResult()
		use_not = False
		#while True:
		if self.current_tok.matches(TOKEN_KEYWORD, 'not'):
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()

			node = res.register(self.comp_expr())
			if res.error: return res
			return res.success(UnaryOpNode(op_tok, node))
		
		node = res.register(self.bin_op(self.arith_expr, (TOKEN_EE, TOKEN_NE, TOKEN_LT, TOKEN_GT, TOKEN_LTE, TOKEN_GTE)))

		if res.error:
			return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, identifier, '+', '-', '(' or '!in'"))

		return res.success(node)


	def func_def(self):
		res = ParseResult()

		if not self.current_tok.matches(TOKEN_KEYWORD, 'func'):
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				f"Expected 'func'"
			))

		res.register_advancement()
		self.advance()

		if self.current_tok.type == TOKEN_IDENTIFIER:
			var_name_tok = self.current_tok
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TOKEN_LPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected '('"
				))
		else:
			var_name_tok = None
			if self.current_tok.type != TOKEN_LPAREN:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected identifier or '('"
				))

		res.register_advancement()
		self.advance()
		arg_name_tock = []
		if self.current_tok.type == TOKEN_IDENTIFIER:
			arg_name_tock.append(self.current_tok)
			res.register_advancement()
			self.advance()

			while self.current_tok.type == TOKEN_COMMA:
				res.register_advancement()
				self.advance()

				if self.current_tok.type != TOKEN_IDENTIFIER:
					return res.failrule(IllegalSyntaxError(
						self.current_tok.pos_start, self.current_tok.pos_end,
						f"Expected identifier"
					))

				arg_name_tock.append(self.current_tok)
				res.register_advancement()
				self.advance()
			if self.current_tok.type != TOKEN_RPAREN:
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected ',' or ')'"
				))
		else:
			if self.current_tok.type != TOKEN_RPAREN:
				return res.failrule(IllegalSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					f"Expected identifier or ')'"
				))
		res.register_advancement()
		self.advance()
		if self.current_tok.type == TOKEN_ARROW:
			res.register_advancement()
			self.advance()
			node_to_return = res.register(self.expr())
			if res.error: return res

			return res.success(FuncDefNode(
				var_name_tok,
				arg_name_tock,
				node_to_return,
				True
			))
		if not self.current_tok.matches(TOKEN_KEYWORD, '{'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '->' or {"
			))

		res.register_advancement()
		self.advance()

		body = res.register(self.statements())
		if res.error: return res

		if not self.current_tok.matches(TOKEN_KEYWORD, '}'):
			return res.failrule(IllegalSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '}'"
			))

		res.register_advancement()
		self.advance()
    
		return res.success(FuncDefNode(
			var_name_tok,
			arg_name_tock,
			body,
			False
		))

	def term(self):
		return self.bin_op(self.factor, (TOKEN_MUL, TOKEN_DIV, TOKEN_REDIV, TOKEN_DIVA))

	def arith_expr(self):
		return self.bin_op(self.term, (TOKEN_PLUS, TOKEN_MINUS))

	def expr(self):
		res = ParseResult()
		if self.current_tok.matches(TOKEN_KEYWORD, 'use'):
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TOKEN_STRING:
				return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

			modul_name = self.current_tok   
			res.register_advancement()
			self.advance()

			#expr = res.register(self.expr())
			if res.error: return res
			return res.success(UseNode(modul_name))

		elif self.current_tok.matches(TOKEN_KEYWORD, 'connect'):
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TOKEN_STRING:
				return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

			connect_name = self.current_tok   
			res.register_advancement()
			self.advance()

			#expr = res.register(self.expr())
			if res.error: return res
			return res.success(UseNode(connect_name, True))

		elif self.current_tok.matches(TOKEN_KEYWORD, 'var'):
			res.register_advancement()
			self.advance()
			if self.current_tok.type != TOKEN_IDENTIFIER:
				return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier"))

			var_name = self.current_tok   
			res.register_advancement()
			self.advance()
			#res.register(self.advance())
			#print(f'{self.current_tok}:{TOKEN_EQ}')
			if self.current_tok.type != TOKEN_EQ:
				return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '='"))

			res.register_advancement()
			self.advance()
			expr = res.register(self.expr())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expr))

		node =  res.register(self.bin_op(self.comp_expr, ((TOKEN_KEYWORD, 'and'), (TOKEN_KEYWORD, 'or'), (TOKEN_KEYWORD, 'in'), (TOKEN_KEYWORD, '!in'))))

		if res.error: 
			return res.failrule(IllegalSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected 'var', int, float, identifier, '+', '-' or '('"))

		return res.success(node)

	def bin_op(self, func_a, ops, func_b=None):
		if func_b == None:
			func_b = func_a
		
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
			op_tok = self.current_tok
			res.register_advancement()
			self.advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)
