# Jihu Mun
# 111623901

from tokens import *
import ply.lex as lex
import ply.yacc as yacc
import sys


# FUNCTIONS
class Function():  # A FUNCTION DECLARATION
    def __init__(self, name, args, block, expr):
        self.name = name
        self.args = args
        self.block = block
        self.expr = expr

    def execute(self):
        # 1. Add the function name to the referencing environment
        functions[self.name] = self

        # 2. Check for errors
        if not type(self.block) == Block:
            p_error()


class FunctionCall(): # CALLING A FUNCTION
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def evaluate(self):
        # 1. Check if the function exists
        if not self.name in functions:
            semantic_error()
        func = functions[self.name]

        # 2. Check for number of arguments
        if not len(func.args) == len(self.args):
            semantic_error()

        # 3. Create local referencing environment and add function args to it.
        names.insert(0, {})
        for i in range(len(self.args)):
            names[0][func.args[i]] = self.args[i].evaluate()

        # 4. Execute the function block and return the expression
        func.block.execute()
        return_value = func.expr.evaluate()

        names.pop(0)
        return return_value


# STATEMENTS
class Assignment():
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def execute(self):
        result = self.expr.evaluate()

        if result is None:
            semantic_error()
        else:
            # Look for the name starting from top of the stack
            for i in range(len(names)):
                if self.var.name in names[i]:
                    names[i][self.var.name] = self.expr.evaluate()
                    return

            # If not found, create a binding in the referencing environment
            names[0][self.var.name] = self.expr.evaluate()


class AssignmentIndex():
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def execute(self):
        # self.var is a ListIndexing object
        # Get the actual variable to update
        self.var.evaluate()
        var_name = self.var.indices[0].name

        # Try to find var_name in names
        scope = 0
        found = False

        for i in range(len(names)):
            if var_name in names[i]:
                var_content = names[i][var_name]
                found = True
                scope = i
                break

        if not found:
            semantic_error()

        try:
            indices = self.var.indices[1:]
            temp = var_content

            for i in indices[:-1]:
                temp = temp[i]

            temp[indices[-1]] = self.expr.evaluate()
        except IndexError:
            semantic_error()

        # Update the variable
        names[scope][var_name] = var_content


class Print():
    def __init__(self, expr):
        self.expr = expr

    def execute(self):
        print(self.expr.evaluate())


class Block():
    def __init__(self, statements):
        self.statements = statements

    def execute(self):
        for s in self.statements:
            s.execute()


class If():
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def execute(self):
        if not type(self.block) == Block:
            p_error()

        val = self.expr.evaluate()

        if not type(val) == bool:
            semantic_error()

        if val:
            self.block.execute()


class IfElse():
    def __init__(self, expr, if_block, else_block):
        self.expr = expr
        self.if_block = if_block
        self.else_block = else_block

    def execute(self):
        if not (type(self.if_block) == Block and type(self.else_block) == Block):
            p_error()

        val = self.expr.evaluate()

        if not type(val) == bool:
            semantic_error()

        if val:
            self.if_block.execute()
        else:
            self.else_block.execute()


class While():
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def execute(self):
        if not type(self.block) == Block:
            p_error()

        while (True):
            val = self.expr.evaluate()

            if not type(val) == bool:
                semantic_error()
            if not val:
                break

            self.block.execute()


# EXPRESSIONS
class Expr():
    def __init__(self):
        self.parent = None

    def evaluate(self):
        pass


# DATA TYPES
class Literal(Expr):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def evaluate(self):
        return self.value


class Variable(Expr):
    def __init__(self, name=""):
        super().__init__()
        self.name = name

    def evaluate(self):
        for i in range(len(names)):
            if self.name in names[i]:
                return names[i][self.name]

        return None


class MyTuple(Expr):
    def __init__(self, expressions=()):
        super().__init__()
        self.expressions = expressions

    def evaluate(self):
        result = []

        for expr in self.expressions:
            result.append(expr.evaluate())

        return tuple(result)


class MyList(Expr):
    def __init__(self, expressions=[]):
        super().__init__()
        self.expressions = expressions

    def evaluate(self):
        result = []

        for expr in self.expressions:
            result.append(expr.evaluate())

        return result


# ARITHMETICS
class Addition(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        v1 = self.left.evaluate()
        v2 = self.right.evaluate()

        if (type(v1) == int or type(v1) == float) and (type(v2) == int or type(v2) == float) or (type(v1) == str and type(v2) == str) or (type(v1) == list and type(v2) == list):
            return v1 + v2
        else:
            semantic_error()


class Subtraction2(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        v1 = self.left.evaluate()
        v2 = self.right

        # Make sure left value is integer or float
        if not (type(v1) == int or type(v1) == float):
            p_error()
        else:
            return v1 - v2


class IntFloatOperation(Expr):
    def __init__(self, left, right, type):
        super().__init__()
        self.left = left
        self.right = right
        self.type = type

    def evaluate(self):
        v1 = self.left.evaluate()
        v2 = self.right.evaluate()

        # Make sure both expressions are integers or floats
        if not (type(v1) == int or type(v1) == float):
            semantic_error()
        if not (type(v2) == int or type(v2) == float):
            semantic_error()
        else:
            if self.type == "SUBTRACTION":
                return v1 - v2
            elif self.type == "MULTIPLICATION":
                return v1 * v2
            elif self.type == "DIVISION":
                return v1 / v2
            elif self.type == "POWER":
                return v1 ** v2


class IntDivOperation(Expr):
    def __init__(self, left, right, type):
        super().__init__()
        self.left = left
        self.right = right
        self.type = type

    def evaluate(self):
        v1 = self.left.evaluate()
        v2 = self.right.evaluate()

        if not (type(v1) == int and type(v2) == int):
            semantic_error()

        else:
            if v2 == 0:
                semantic_error()
            else:
                if self.type == "DIVISION":
                    return v1 // v2
                elif self.type == "MODULO":
                    return v1 % v2


# LIST AND TUPLE STUFF
class ListIndexing(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        v1 = self.left.evaluate()  # Should be list or str
        v2 = self.right.evaluate()  # Should be int

        if not (type(v1) == list or type(v1) == str):
            semantic_error()

        # Make sure the second expr is an integer
        elif not type(v2) == int:
            semantic_error()

        else:
            if v2 < 0 or v2 >= len(v1):
                semantic_error()
            else:
                if type(self.left) == Variable:
                    self.indices = [self.left] + [self.right.evaluate()]
                elif type(self.left) == ListIndexing:
                    self.indices = self.left.indices + [self.right.evaluate()]

                return v1[v2]


class TupleIndexing(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        v1 = self.left.evaluate()  # Should be int
        v2 = self.right.evaluate()  # Should be tuple

        if not (type(v1) == int and type(v2) == tuple):
            semantic_error()

        else:
            index = v1 - 1
            if index < 0 or index >= len(v2):
                semantic_error()
            else:
                return v2[index]


class Membership(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        # Either expr in list or string in string
        v1 = self.left.evaluate()
        v2 = self.right.evaluate()

        if type(v2) == list:
            return v1 in v2
        elif type(v2) == str and type(v1) == str:
            return v1 in v2
        else:
            semantic_error()


class Cons(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def evaluate(self):
        v1 = self.left.evaluate()  # Anything
        v2 = self.right.evaluate()  # List

        if not type(v2) == list:
            semantic_error()
        else:
            return [v1] + v2


class Not(Expr):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def evaluate(self):
        v1 = self.expr.evaluate()

        if not type(v1) == bool:
            semantic_error()
        else:
            return not v1


class BinaryBooleanOperation(Expr):
    def __init__(self, left, right, type):
        super().__init__()
        self.left = left
        self.right = right
        self.type = type

    def evaluate(self):
        v1 = self.left.evaluate()

        if not type(v1) == bool:
            semantic_error()

        if self.type == 'and':
            if not v1:
                return False
            else:
                v2 = self.right.evaluate()
                if not type(v2) == bool:
                    semantic_error()

                return v2

        elif self.type == 'or':
            if v1:
                return True
            else:
                v2 = self.right.evaluate()
                if not type(v2) == bool:
                    semantic_error()

                return v2


class Comparison(Expr):
    def __init__(self, left, right, type):
        super().__init__()
        self.left = left
        self.right = right
        self.type = type

    def evaluate(self):
        v1 = self.left.evaluate()
        v2 = self.right.evaluate()

        if (type(v1) == int or type(v1) == float) and (type(v2) == int or type(v2) == float) or (type(v1) == str and type(v2) == str):
            if self.type == 'ge':
                return v1 >= v2
            elif self.type == 'gt':
                return v1 > v2
            elif self.type == 'le':
                return v1 <= v2
            elif self.type == 'lt':
                return v1 < v2
            elif self.type == 'eq':
                return v1 == v2
            elif self.type == 'ne':
                return not (v1 == v2)

        else:
            semantic_error()


# sbml.py
lexer = lex.lex()


# GRAMMAR FOR PARSING
def p_program(p):
    'program : functions LBRACE stmts RBRACE'
    p[0] = p[1] + p[3]


def p_functions_empty(p):
    'functions :'
    p[0] = []


def p_functions_nonempty(p):
    'functions : function functions'
    p[0] = [p[1]] + p[2]


def p_function_noargs(p):
    'function : FUNCTION VARIABLE LPAREN RPAREN ASSIGN stmt expr SEMICOLON'
    p[0] = Function(p[2], (), p[6], p[7])


def p_function_args(p):
    'function : FUNCTION VARIABLE LPAREN VARIABLE args RPAREN ASSIGN stmt expr SEMICOLON'
    p[0] = Function(p[2], (p[4],) + p[5], p[8], p[9])


def p_expr_functioncall_noargs(p):
    'expr : VARIABLE LPAREN RPAREN'
    p[0] = FunctionCall(p[1], ())


def p_expr_functioncall_args(p):
    'expr : VARIABLE LPAREN expr exprtail RPAREN'
    p[0] = FunctionCall(p[1], (p[3], ) + p[4])


def p_args_empty(p):
    'args :'
    p[0] = ()


def p_args_nonempty(p):
    'args : COMMA VARIABLE args'
    p[0] = (p[2],) + p[3]


def p_stmts_empty(p):
    'stmts :'
    p[0] = []


def p_stmts_nonempty(p):
    'stmts : stmt stmts'
    p[0] = [p[1]] + p[2]


def p_expr_variable(p):
    'expr : VARIABLE'
    p[0] = Variable(p[1])


def p_expr_num(p):
    'expr : number %prec NUM'
    p[0] = Literal(p[1])


def p_number_i(p):
    'number : INTEGER'
    p[0] = p[1]


def p_number_r(p):
    'number : REAL'
    p[0] = p[1]


def p_expr_string(p):
    'expr : STRING'
    p[0] = Literal(p[1])


def p_expr_bool(p):
    'expr : BOOLEAN'
    p[0] = Literal(p[1])


def p_stmt_assign(p):
    'stmt : expr ASSIGN expr SEMICOLON'
    if type(p[1]) == ListIndexing:
        p[0] = AssignmentIndex(p[1], p[3])
    else:
        p[0] = Assignment(p[1], p[3])


def p_stmt_print(p):
    'stmt : PRINT expr RPAREN SEMICOLON'
    p[0] = Print(p[2])


def p_stmt_block(p):
    'stmt : LBRACE stmts RBRACE'
    p[0] = Block(p[2])


def p_stmt_if(p):
    'stmt : IF expr RPAREN stmt %prec IFNORMAL'
    p[0] = If(p[2], p[4])


def p_stmt_ifelse(p):
    'stmt : IF expr RPAREN stmt ELSE stmt'
    p[0] = IfElse(p[2], p[4], p[6])


def p_stmt_while(p):
    'stmt : WHILE expr RPAREN stmt'
    p[0] = While(p[2], p[4])


def p_expr_paren(p):
    'expr : LPAREN expr RPAREN %prec PAREN'
    p[0] = p[2]


def p_expr_emptytuple(p):
    'expr : LPAREN RPAREN %prec TUPLEINIT'
    p[0] = MyTuple()


def p_expr_nonemptytuple(p):
    'expr : LPAREN expr COMMA expr exprtail RPAREN %prec TUPLEINIT'
    p[0] = MyTuple((p[2], p[4]) + p[5])


def p_exprtail_nonempty(p):
    'exprtail : COMMA expr exprtail'
    p[0] = (p[2],) + p[3]


def p_exprtail_empty(p):
    'exprtail : %prec EXPRTAILEMPTY'
    p[0] = ()


def p_expr_tupleindexing(p):
    'expr : SHARP LPAREN expr RPAREN expr %prec TUPLEINDEXING'
    # Make sure index is an integer
    p[0] = TupleIndexing(p[3].value, p[5])


def p_expr_tupleindexing2(p):
    'expr : SHARP number expr %prec TUPLEINDEXING'
    # Make sure index is an integer
    p[0] = TupleIndexing(p[2], p[3])


def p_expr_listindexing(p):
    'expr : expr LBRACKET expr RBRACKET %prec LISTINDEXING'
    # Make sure first expr is a list or string
    p[0] = ListIndexing(p[1], p[3])


def p_expr_emptylist(p):
    'expr : LBRACKET RBRACKET %prec LISTINIT'
    p[0] = MyList()


def p_expr_nonemptylist(p):
    'expr : LBRACKET expr exprtail RBRACKET %prec LISTINIT'
    p[0] = MyList([p[2]] + list(p[3]))


def p_expr_exponent(p):
    'expr : expr POWER expr'
    p[0] = IntFloatOperation(p[1], p[3], type="POWER")


def p_expr_mult(p):
    'expr : expr MULT expr'
    p[0] = IntFloatOperation(p[1], p[3], type="MULTIPLICATION")


def p_expr_div(p):
    'expr : expr DIV expr'
    p[0] = IntFloatOperation(p[1], p[3], type="DIVISION")


def p_expr_intdiv(p):
    'expr : expr INTDIV expr'
    p[0] = IntDivOperation(p[1], p[3], type="DIVISION")


def p_expr_mod(p):
    'expr : expr MOD expr'
    p[0] = IntDivOperation(p[1], p[3], type="MODULO")


def p_expr_add(p):
    'expr : expr ADD expr'
    p[0] = Addition(p[1], p[3])


def p_expr_sub(p):
    'expr : expr SUB expr'
    p[0] = IntFloatOperation(p[1], p[3], 'SUBTRACTION')


def p_number_negation(p):
    'number : USUB number %prec UMINUS'
    if not (type(p[2]) == int or type(p[2]) == float):
        p_error()
    else:
        p[0] = -p[2]


def p_expr_sub2(p):
    'expr : expr USUB number %prec SUBU'
    p[0] = Subtraction2(p[1], p[3])


def p_expr_in(p):
    'expr : expr IN expr'
    p[0] = Membership(p[1], p[3])


def p_expr_cons(p):
    'expr : expr CONS expr'
    p[0] = Cons(p[1], p[3])


def p_expr_not(p):
    'expr : NOT expr'
    p[0] = Not(p[2])


def p_expr_and(p):
    'expr : expr AND expr'
    p[0] = BinaryBooleanOperation(p[1], p[3], 'and')


def p_expr_or(p):
    'expr : expr OR expr'
    p[0] = BinaryBooleanOperation(p[1], p[3], 'or')


def p_expr_ge(p):
    'expr : expr GE expr'
    p[0] = Comparison(p[1], p[3], 'ge')


def p_expr_gt(p):
    'expr : expr GT expr'
    p[0] = Comparison(p[1], p[3], 'gt')


def p_expr_le(p):
    'expr : expr LE expr'
    p[0] = Comparison(p[1], p[3], 'le')


def p_expr_lt(p):
    'expr : expr LT expr'
    p[0] = Comparison(p[1], p[3], 'lt')


def p_expr_eq(p):
    'expr : expr EQ expr'
    p[0] = Comparison(p[1], p[3], 'eq')


def p_expr_ne(p):
    'expr : expr NE expr'
    p[0] = Comparison(p[1], p[3], 'ne')


def p_error(p=None):
    raise ParsingError("SYNTAX ERROR")


def semantic_error():
    raise ParsingError("SEMANTIC ERROR")


precedence = (
    ('right', 'IFNORMAL', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'GT', 'GE', 'NE', 'EQ', 'LE', 'LT'),  # Comparisons
    ('right', 'CONS'),
    ('left', 'IN'),
    ('left', 'ADD', 'SUB', 'SUBU'),
    ('left', 'MOD', 'INTDIV', 'DIV', 'MULT'),
    ('right', 'POWER'),
    ('left', 'EXPRTAILEMPTY'),
    ('left', 'LISTINDEXING', 'LBRACKET', 'RBRACKET'),
    ('left', 'ASSIGN'),
    ('left', 'TUPLEINDEXING'),
    ('left', 'TUPLEINIT', 'LISTINIT'),
    ('left', 'PAREN'),
    ('right', 'UMINUS'),
    ('left', 'NUM'),
    ('left', 'INTEGER', 'REAL')
)

parser = yacc.yacc()

# Get the file name
filename = sys.argv[1]

with open(filename) as f:
    program = ""

    for line in f:
        program += line

    try:
        # Dictionary of names
        names = [{}]  # This is a stack, with most specific referencing environment coming first
        functions = {}

        result = parser.parse(program)

        for stmt in result:
            stmt.execute()

    except ParsingError as e:
        print(e)
