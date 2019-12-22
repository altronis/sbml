class ParsingError(Exception):
    pass


# List of token names
tokens = (
    'LPAREN',
    'RPAREN',
    'COMMA',
    'SHARP',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'POWER',
    'MULT',
    'DIV',
    'INTDIV',
    'MOD',
    'ADD',
    'SUB',
    'USUB',
    'IN',
    'CONS',
    'NOT',
    'AND',
    'OR',
    'LT',
    'LE',
    'EQ',
    'NE',
    'GE',
    'GT',
    'INTEGER',
    'REAL',
    'BOOLEAN',
    'STRING',
    'SEMICOLON',
    'PRINT',
    'VARIABLE',
    'ASSIGN',
    'IF',
    'ELSE',
    'WHILE',
    'FUNCTION'
)

t_SEMICOLON = r'\s*;\s*'
t_LPAREN = r'\s*\(\s*'
t_RPAREN = r'\s*\)\s*'
t_COMMA = r'\s*\,\s*'
t_SHARP = r'\s*\#\s*'
t_LBRACKET = r'\s*\[\s*'
t_RBRACKET = r'\s*\]\s*'
t_LBRACE = r'\s*{\s*'
t_RBRACE = r'\s*}\s*'
t_POWER = r'\s*\*\*\s*'
t_MULT = r'\s*\*\s*'
t_DIV = r'\s*\/\s*'
t_ADD = r'\s*\+\s*'
t_SUB = r'\s*\-\ +'
t_USUB = r'\s*\-'
t_CONS = r'\s*::\s*'
t_ASSIGN = r'\s*=\s*'
t_LT = r'\s*<\s*'
t_LE = r'\s*<=\s*'
t_EQ = r'\s*==\s*'
t_NE = r'\s*<>\s*'
t_GE = r'\s*>=\s*'
t_GT = r'\s*>\s*'
t_VARIABLE = r'[a-zA-Z][a-zA-Z0-9_]*'

t_ignore = '\n'


# Keywords
def t_PRINT(t):
    r'print\s*\('
    return t


def t_IF(t):
    r'if\s*\('
    return t


def t_ELSE(t):
    r'\s*else\s*'
    return t


def t_WHILE(t):
    r'while\s*\('
    return t


def t_FUNCTION(t):
    r'\s*fun\s*'
    return t


def t_INTDIV(t):
    r'\s*div\s*'
    return t


def t_MOD(t):
    r'\s*mod\s*'
    return t


def t_IN(t):
    r'\s*in\s*'
    return t


def t_NOT(t):
    r'\s*not\s*'
    return t


def t_OR(t):
    r'\s*orelse\s*'
    return t


def t_AND(t):
    r'\s*andalso\s*'
    return t


def t_REAL(t):
    r'((\d+\.\d*)|(\d*\.\d+))(e-?\d+)?'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'(True) | (False)'
    t.value = eval(t.value)
    return t


def t_STRING(t):
    r'(\"[^\"]*\")|(\'[^\']*\')'
    t.value = t.value[1: -1]
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    if t.value[0].strip() == '':
        t.lexer.skip(1)
    else:
        raise ParsingError("SYNTAX ERROR")
