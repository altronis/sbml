# sbml
SBML (Stony Brook ML) is a programming language that is a hybrid of Python and SML. It is written with PLY.

## Requirements
python 3.7  
PLY

## How to run
`python sbml.py <filename>`

## Program
An input program might contain multiple function definitions followed by a single main block that gets executed.

## Data Types
The data types in SBML are integer, real, boolean, list and tuple.

### Integer
Positive (no sign) or negative (unary -) whole numbers in base-10 representation (decimal representation). An integer literal is one or more digits, 0-9. Examples: 57, -18, 235

### Real
A real value is represented by 0 or more digits (0-9), followed by a decimal point, ".", followed by 0 or more digits (0-9), except that a decimal point by itself with no leading or trailing digit is not a real.  
Examples: 3.14159, 0.7, .892, 32787.          

A real can also contain exponents as in scientific notation. In this case, a real value, as defined above, is followed by an "e" character and then a positive or negative integer, as defined above.  
Examples: 6.02e-23, 17.0e4

### Boolean
True, False (just like in Python).

### String
A string literal begins with a single or double quote, followed by zero or more non-quote characters, and ends with a matching quote. The          value of the string literal does not include the starting and ending quotes.  
Examples: "Hello World!", "867-5309"

### List
A list literal is composed by a left square bracket, followed by a comma-separated sequence of zero or more expressions, followed by a right square bracket.  
Examples: ["a", "b"], [1, 2], [307, "307", 304+3]

## Operators

| Operator                        | Description                                                                                          |
|---------------------------------|------------------------------------------------------------------------------------------------------|
| (expression)                    | A paranthesized expression                                                                           |
| (expression1, expression2, ...) | Tuple constructor                                                                                    |
| #i(tuple)                       | returns the argument at index i in the tuple. Indices start at 1.                                    |
| a[b]                            | Indexing operation. b can be any expression.                                                         |
| a ** b                          | Exponentiation. base a raised to the power b. Right associative.                                     |
| a * b                           | Multiplication. Overloaded for integers and reals.                                                   |
| a / b                           | Division. Overloaded for integers and reals, but result is a real.                                   |
| a div b                         | Integer division. Returns the quotient.                                                              |
| a mod b                         | Returns the remainder of a div b.                                                                    |
| a + b                           | Addition. Overloaded for integers, reals, strings and lists.                                         |
| a - b                           | Subtraction. Overloaded for integers and reals.                                                      |
| a in b                          | Membership. Evaluates to True if it finds the value of a inside the string or list represented by b. |
| a :: b                          | Cons. Adds operand a to the front of the list b.                                                     |
| not a                           | Boolean negation.                                                                                    |
| a andalso b                     | Boolean AND.                                                                                         |
| a orelse b                      | Boolean OR.                                                                                          |
| a < b                           | Less than.                                                                                           |
| a <= b                          | Less than or equal to.                                                                               |
| a == b                          | Equal to.                                                                                            |
| a <> b                          | Not equal to.                                                                                        |
| a >= b                          | Greater than or equal to.                                                                            |
| a > b                           | Greater than.                                                                                        |

## Semantics

### Indexing
Operand a must be either a string or a list. Operand b must be an integer. If a is a string, then return the b-th character as a string. If it is a list, then return the b-th element of the list. The index starts at 0. If the index is out of bounds, then it is a semantic error.

### Addition
Operands must either both be numbers, or both strings, or both be lists. If they are both strings, then string concatenation is performed. If a and b are both lists, then list concatenation is performed.

### Comparisons
Operands must either both be numbers or both be strings. Comparison of strings follows lexicographic order.

## Statements

### Block
A block statement consists of zero or more statements enclosed in curly-braces, "{...}". When the block executes, each of the statements is executed in sequential order.

### Variables and assignment
Variable names begin with an alphabet letter, which may be followed by zero or more letters, digits or underscores.

An assignment statement consists of a variable (or an indexed list variable) , an equals sign, an expression, and a semicolon, "var = exp;". The left-hand side expression is assigned the value evaluated for the right-hand side expression.

### Print
A print statement consists of the "print" keyword, a left parenthesis, an expression, a right parenthesis, and then a semicolon. When the statement executes, the expression is evaluated for its value. 

### If statement
Consists of a keyword "if", a left parenthesis, an expression, a right parenthesis, and a block statement as the body of the If statement. When the If statement executes, if the expression evaluates to True, then the block statement composing the body is executed.

### If-Else Statement
Consists of a keyword "if", a left parenthesis, an expression, a right parenthesis, a block statement as the body of the If clause, the keyword "else", and a block statement as the body of the Else clause. 

When the If-Else statement executes, if the expression is True, then execute the block statement that is the body of the If clause. Otherwise, execute the block statement that is the body of the Else clause.

### While Loop
A While statement consists of the keyword "while", a left parenthesis, an expression, a right parenthesis, and a block statement that is the body of the While statement.

Executing the while statement begins by evaluating the condition expression for its value. If the expression evaluates to False, then the While statement terminates. Otherwise, execute the block of statements that compose the body of the While statement, and then repeat the execution of the While statement from the evaluation of the condition expression.

## Functions

### Function Definition
A function definition begins with the keyword "fun", followed by the name of the function, a left parenthesis, variables representing formal parameters separated by commas, a right parenthesis, an equal sign, a block, and then an expression. 

When the function is called, the block is executed first. Then the expression is evaluated and the result of the expression evaluation is returned to the caller.

### Function Call
A function call is an expression. The function name is followed by a left parenthesis, and then argument expression, followed by a right parenthesis. 

The number of arguments passed to the call must match the number of parameters in the function definition.
