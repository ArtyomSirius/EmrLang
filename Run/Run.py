from Lexer.Lexer import *
from Parser.Parser import *
from Interpreter.Interpreter import *
from Interpreter.SymbolTable import *
from Errors.Errors import *

global_symbol_table.set("null", Number.null)
global_symbol_table.set("None", Number(0))
global_symbol_table.set("true", Number.false)
global_symbol_table.set("false", Number.true)
global_symbol_table.set("Panda_Secret", String("А вот секретик, с добрым полдником!"))
global_symbol_table.set("Lia", String("Лия, скинь расписание(секретик)"))

global_symbol_table.set("mathPi", Number.math_pi)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("inputInt", BuiltInFunction.input_int)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("quit", BuiltInFunction.quit)
global_symbol_table.set("help", BuiltInFunction.help)
global_symbol_table.set("rstrip", BuiltInFunction.Rstrip)
global_symbol_table.set("lstrip", BuiltInFunction.Lstrip)
global_symbol_table.set("open", BuiltInFunction.open_file)
global_symbol_table.set("write", BuiltInFunction.write)
global_symbol_table.set("TraceBack", BuiltInFunction.tracebackerr)
global_symbol_table.set("run", BuiltInFunction.run)

def run(fn, text):
	# Generate tokens
	  lexer = Lexer(fn, text)
	  tokens, error = lexer.make_tokens()
	  if error: return None, error
	  #print("Lexer[OK]")
	  #print(tokens)
	  # Generate AST
	  parser = Parser(tokens)
	  ast = parser.parse()
	  if ast.error: 
	  	return None, ast.error

	  #print(ast.node)
	  # Run program
	  interpreter = Interpreter()
	  context = Context('<program>')
	  context.symbol_table = global_symbol_table
	  result = interpreter.visit(ast.node, context)
	  return result.value, result.error