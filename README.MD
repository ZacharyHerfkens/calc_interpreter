# Calc language REPL and interpreter

A simple assignment/expression language. 

A program consists of assignment statements of the form "{id} = {expr}"
where {expr} is a standard expression consisting of:
- binary operators:
    - '+' addition
    - '-' subtraction
    - '*' multiplication
    - '/' division
- unary operators:
    - '+' positive (no op)
    - '-' negation
- parenthesis '(' - ')'

When provided with a file as an argument, the interpreter will interpret the contents of the file
as a series of statements, and print the resulting environment (a dictionary of id's and values)

When not provided a file, the repl will start. Assignment statements may be entered one at a time
and their results will be printed, and their assingments saved to the environment.