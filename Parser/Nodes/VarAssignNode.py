class VarAssignNode:
	def __init__(self, var_name_tok, value_node, const=None, cl=[]):
		self.var_name_tok = var_name_tok
		self.value_node = value_node
		self.cl = cl

		self.const = const
		#self.cl.append(var_name_tok)

		self.pos_start = self.var_name_tok.pos_start
		self.pos_end = self.value_node.pos_end