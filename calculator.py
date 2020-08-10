import  string
from collections import deque
operators = {'+': 1, '-': 1, "*": 2, '/': 2, '^': 3}

defined_variables = {}
variables = {}
stack = []
result = deque()

def var_definition(expression):
    global variables
    var_name = ''
    try:
        left_side, right_side = expression.split('=')
    except ValueError:
        print('Invalid assignment')
        return
    left_side = left_side.lstrip(' ').rstrip(' ')
    for pos, char in enumerate(left_side):
        if char in string.ascii_letters:
            var_name += char
        else:
            print('Invalid identifier')
            return
    try:
        right_side = calculate(parsing(right_side))
    except ValueError:
        print('Unknown variable')
    variables[var_name] = right_side


def formatting(expression):
    replacements = [("--", "+"), ("+-", "-"), ("-+", "-"), ("++", "+")]
    while any(pattern[0] in expression for pattern in replacements):
            for pattern in replacements:
                expression = expression.replace(*pattern)

    num_temp = []
    res = []
    for pos, char in enumerate(expression):
        if char in string.digits or char in string.ascii_letters:
            num_temp.append(char)
            if pos == len(expression) - 1:
                res.append(num_temp)
        elif char == ' ':
            res.append(num_temp)
            num_temp = []
        elif char in operators or char == '(' or char == ')':
            res.append(num_temp)
            num_temp = []
            num_temp.append(char)
            res.append(num_temp)
            num_temp = []
        if (char == '*' and expression[pos - 1] == '*') or (char == '/' and expression[pos - 1] == '/') or (char == '^' and expression[pos - 1] == '^'):
            return 'Invalid expression'
    while not all(res):
        res.remove([])

    for pos, item in enumerate(res):
        res[pos] = ''.join(item)

    for pos, item in enumerate(res):
        if item in variables:
            res[pos] = variables[item]
    return res



def postfixing(expression):
    result.clear()
    stack.clear()
    for pos, element in enumerate(expression):
        if element not in operators and element != '(' and element != ')':
            result.append(element)
        else:
            if len(stack) == 0 or stack[-1] == '(':
                stack.append(element)
            elif element == '(':
                stack.append(element)
            elif element == ')':
                while stack[-1] != '(':
                    result.append(stack.pop())
                stack.pop()
            elif operators[element] > operators[stack[-1]]:
                stack.append(element)
            elif operators[element] <= operators[stack[-1]]:
                while True:
                        if operators[element] > operators[stack[-1]] or stack[-1] == '(':
                            stack.append(element)
                            break
                        else:
                            result.append(stack.pop())
                        if len(stack) == 0:
                            stack.append(element)
                            break
        if pos == len(expression) - 1:
            while len(stack) > 0:
                result.append(stack.pop())
    return result

def parsing(expression):
    formatted_expression = formatting(expression)
    postfixed_expression = postfixing(formatted_expression)
    return postfixed_expression


def calculate(postfixed_exp):
    if postfixed_exp == deque(['I', 'n', 'v', 'a', 'l', 'i', 'd', ' ', 'e', 'x', 'p', 'r', 'e', 's', 's', 'i', 'o', 'n']):
        return 'Invalid expression'
    for pos, element in enumerate(postfixed_exp):
        if element in operators:
            op1 = stack.pop()
            op2 = stack.pop()
            if element == '+':
                stack.append(op1 + op2)
            elif element == '-':
                stack.append(op2 - op1)
            elif element == '*':
                stack.append(op1 * op2)
            elif element == '/':
                stack.append(op2 / op1)
            elif element == '^':
                stack.append(op2 ** op1)
        else:
            stack.append(int(element))
    return int(stack.pop())

def menu():
        user_input = input()
        if user_input == '' or user_input == ' ':
            return
        elif user_input[0] == '/':
            if user_input == "/exit":
                print('Bye!')
                quit()
            if user_input == "/help":
                print('The program calculates the sum and difference of numbers.')
                return
            else:
                print('Unknown command')
                return
        if '=' in user_input:
            var_definition(user_input)
        elif '+' in user_input or '-' in user_input or '*' in user_input or '/' in user_input or '^' in user_input:
            if user_input.count('(') != user_input.count(')'):
                print('Invalid expression')
            else:
                print(calculate(parsing(user_input)))
        else:
            try:
                print(variables[user_input.lstrip(' ').rstrip(' ')])
            except KeyError:
                print('Unknown variable')

while True:
    menu()
