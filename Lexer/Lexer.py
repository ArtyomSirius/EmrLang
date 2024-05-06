from Lexer.Token import *
from Lexer.Position import *
from Errors.Errors import *

class Lexer():
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)
		self.current_char = None
		self.advance()


	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char in ' ':
				self.advance()
			elif self.current_char in ';\n':
				tokens.append(Token(TOKEN_NEWLINE, pos_start=self.pos))
				self.advance()
			elif self.current_char == '#':
				self.skip_comment()


			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char == '"':
				token, error = self.make_string()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == "'":
				token, error = self.make_string()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == '+':
				tokens.append(Token(TOKEN_PLUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(self.make_minus_or_arrow())
			elif self.current_char == '*':
				tokens.append(Token(TOKEN_MUL, pos_start=self.pos))
				self.advance()
			elif self.current_char == '/':

				tokens.append(Token(TOKEN_DIV, pos_start=self.pos))
				self.advance()
			elif self.current_char == '\\':
				tokens.append(Token(TOKEN_DIVA, pos_start=self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TOKEN_POW, pos_start=self.pos))
				self.advance()
			elif self.current_char == '%':
				tokens.append(Token(TOKEN_REDIV, pos_start=self.pos))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TOKEN_LPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TOKEN_RPAREN, pos_start=self.pos))
				self.advance()

			elif self.current_char == '[':
				tokens.append(Token(TOKEN_LSQUARE, pos_start=self.pos))
				self.advance()
			elif self.current_char == ']':
				tokens.append(Token(TOKEN_RSQUARE, pos_start=self.pos))
				self.advance()

			elif self.current_char == '!':
				token, error = self.make_not_equals()
				if error: return [], error
				tokens.append(token)
			elif self.current_char == '=':
				tokens.append(self.make_equals())
				#self.advance()
			elif self.current_char == '<':
				tokens.append(self.make_less_than())
			elif self.current_char == '>':
				tokens.append(self.make_greater_than())
				#self.advance()

			elif self.current_char == ',':
				tokens.append(Token(TOKEN_COMMA, pos_start=self.pos))
				self.advance()
			elif self.current_char == '.':
				tokens.append(Token(TOKEN_POINT, pos_start=self.pos))
				self.advance()

			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

		tokens.append(Token(TOKEN_EOF, pos_start=self.pos))
		return tokens, None


	def skip_comment(self):
		self.advance()
		while self.current_char != '\n':
			self.advance()
		self.advance()

	def make_minus_or_arrow(self):
		tok_type = TOKEN_MINUS
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '>':
			self.advance()
			tok_type = TOKEN_ARROW

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_string(self):
		string = ''
		pos_start = self.pos.copy()
		escape_character = False
		self.advance()

		escape_characters = {
			'n': '\n',
			't': '\t'
		}

		#escape_character = False
		while self.current_char != None and (self.current_char != '"' or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
			else:
				if self.current_char == '\\':
					escape_character = True
				else:
					string += self.current_char
			escape_character = False
			self.advance()

		if self.current_char == '"':
			self.advance()
			return Token(TOKEN_STRING, string, pos_start, self.pos), None

		return None,  ExpectedCharError(pos_start, self.pos, "The required symbol is missing('\"')")

	def make_number(self):
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1:
					break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()

		
		if dot_count == 0:
			return Token(TOKEN_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TOKEN_FLOAT, float(num_str), pos_start, self.pos)

	def make_identifier(self):
		id_str = ''
		pos_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.advance()

		tok_type = TOKEN_KEYWORD if id_str in KEYWORDS else TOKEN_IDENTIFIER
		return Token(tok_type, id_str, pos_start, self.pos)

	def make_not_equals(self):
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			return Token(TOKEN_NE, pos_start=pos_start, pos_end=self.pos), None
		if self.current_char == 'i':
			self.advance()
			if self.current_char == 'n':
				self.advance()
				return Token(TOKEN_KEYWORD, "!in", pos_start, self.pos), None


		self.advance()
		return None, ExpectedCharError(pos_start, self.pos, "'=' or 'in' (after '!')")
	

	def make_equals(self):
		tok_type = TOKEN_EQ
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TOKEN_EE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_less_than(self):
		tok_type = TOKEN_LT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TOKEN_LTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

	def make_greater_than(self):
		tok_type = TOKEN_GT
		pos_start = self.pos.copy()
		self.advance()

		if self.current_char == '=':
			self.advance()
			tok_type = TOKEN_GTE

		return Token(tok_type, pos_start=pos_start, pos_end=self.pos)