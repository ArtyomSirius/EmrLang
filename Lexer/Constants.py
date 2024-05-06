import string

DIGITS           = '1234567890'
LETTERS          = string.ascii_letters + "{" + "}"
LETTERS_DIGITS   = LETTERS + DIGITS

TOKEN_STRING     = "STRING"

TOKEN_IDENTIFIER = 'IDENTIFIER'
TOKEN_EQ         = 'EQ'
TOKEN_KEYWORD    = 'KEYWORD'
TOKEN_INT        = 'INT'
TOKEN_FLOAT      = 'FLOAT'
TOKEN_PLUS       = 'PLUS'
TOKEN_MINUS      = 'MINUS'
TOKEN_MUL        = 'MUL'
TOKEN_DIV        = 'DIV'
TOKEN_REDIV      = 'REDIV'
TOKEN_DIVA       = 'DIVA'
TOKEN_LPAREN     = 'LPAREN'
TOKEN_RPAREN     = 'RPAREN'
TOKEN_LSQUARE    = 'LSQUARE'
TOKEN_RSQUARE    = 'RSQUARE'
TOKEN_POW        = 'POW'
TOKEN_EOF        = 'EOF'

TOKEN_NEWLINE    = 'NEWLINE'

TOKEN_EE         = 'EE'
TOKEN_NE         = 'NE'
TOKEN_LT         = 'LT'
TOKEN_GT         = 'GT'
TOKEN_LTE        = 'LTE'
TOKEN_GTE        = 'GTE'

TOKEN_COMMA      = 'COMMA'
TOKEN_POINT      = 'POINT'
TOKEN_ARROW      = 'ARROW'

KEYWORDS = [
	'var',
	'and',
	'or',
	'not',
	'if',
	'{',
	'elif',
	'else',
	'for',
	'to',
	'in',
	'!in',
	'step',
	'while',
	'not in',
	'func',
	'try',
	'except',
	'}',
	'use',
	'connect',
	'pass',
	'return',
	'continue',
	'break'
]