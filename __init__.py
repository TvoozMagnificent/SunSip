# SLWNSNBP, or "Sun Sip"
# Simple Language Whose Name Should Not Be Pronounced

import random
import math
import sys
import os
import re

def before_run():
    print('\n'*1000)
    if '--help' in sys.argv: print('''
    Syntax: python3 main.py program.slwnsnbp [options]
    Options:
        --help : Print this help message and exit.
        -d     : Debug mode.
        -v     : Verbose mode.
        -w     : Disable warnings.
    '''); sys.exit()

    try:
        file_containing_program = sys.argv[1]
    except IndexError:
        print('\033[91m\nNo program specified.\n'
              'Use the --help option for '
              'usage help.\033[0m\n'); sys.exit()
    debug_mode = '-d' in sys.argv
    disable_warnings = '-w' in sys.argv
    verbose_mode = '-v' in sys.argv

    try:
        with open(file_containing_program, 'r') as f:
            program = f.readlines()
    except FileNotFoundError:
        print(f'\033[91mSorry, I can not find the file: '
              f'{file_containing_program}.'
              f'\nCheck the path, name, and file extension.'
              f'\nFor usage help, use the --help option.\033[0m\n')
        sys.exit()

    return program, debug_mode, disable_warnings, verbose_mode
program, debug_mode, disable_warnings, verbose_mode = before_run()

def parse_program(program):
    program = [i.strip() for i in program]
    program = [[i.split(' ')[0], ' '.join(i.split(' ')[1:])] for i in program]
    program = [[j.strip() for j in i] for i in program]
    return program
program = parse_program(program)
if debug_mode or verbose_mode: print(f'\nProgram:\n{program}\n')

current_line = 0; variables = {}; instructions = parameters = None

def parse_value(value):

    # integer:
    # with one or no '- character and one or more characters from "0123456789"
    # Use re.match to check if the string matches the pattern.

    integer_pattern = r'^-?[0-9]+$'
    if re.match(integer_pattern, value):
        return int(value)

    # float:
    # with one or no '- character, some or no characters from "0123456789",
    #           the '. character, and some or no characters from "0123456789"
    # Use re.match to check if the string matches the pattern.

    float_pattern = r'^-?[0-9]*\.[0-9]*$'
    if re.match(float_pattern, value):
        if value == '.': value = '0.'
        if value == '-.': value = '-0.'
        return float(value)

    # Scientific Notation of integers:
    # with one or no '- character,
    #               one or more characters from "0123456789", the letter "e",
    #           and one or more characters from "0123456789"
    # Use re.match to check if the string matches the pattern.

    scino_int_pattern = r'^-?[0-9]+e[0-9]+$'
    if re.match(scino_int_pattern, value):
        first, second = value.split('e')
        return int(first) * 10 ** int(second)

    # Scientific Notation of floats:
    # with one or no '- character,
    #               some or no characters from "0123456789", one or no '. character,
    #           and some or no characters from "0123456789", the letter "E",
    #           one or no '- character,
    #               some or no characters from "0123456789", one or no '. character,
    #           and some or no characters from "0123456789"
    # Use re.match to check if the string matches the pattern.

    scino_float_pattern = r'^-?[0-9]*\.*[0-9]*E-?[0-9]*\.*[0-9]*$'
    if re.match(scino_float_pattern, value):
        first, second = value.split('E')
        if first == '': first = '0'
        if first == '-': first = '0'
        if first == '.': first = '0'
        if first == '-.': first = '0'
        if second == '': second = '0'
        if second == '-': second = '0'
        if second == '.': second = '0'
        if second == '-.': second = '0'
        return float(first) * 10 ** float(second)

    # string:
    # with one '" character, some or no more characters,
    #           and an optional '" character
    #           To indicate a '" character at the end of string,
    #           end with two double quotes.
    # Use re.match to check if the string matches the pattern.

    string_pattern = r'^".*"?$'
    if re.match(string_pattern, value):
        value = value[1:]
        if value.endswith('"'):
            value = value[:-1]
        return value

    # character:
    # with one '' character, some character, and an optional '' character.
    #           "''" will denote the '' character inside of "".
    # Use re.match to check if the string matches the pattern.

    character_pattern = r'^\'.\'?$'
    if re.match(character_pattern, value):
        value = value[1:]
        return value[0]

    if value == '[]': return list()
    if value == '{}': return set()
    if value == '<>': return list()

    if value == 'y': return True
    if value == 'n': return False

    warn(f'VALUE {value} NOT RECOG AT LINE {current_line+1}')
    return 0
def type_(value, careful=0):
    if careful: return 'int' if value not in variables else type_(variables[value])
    if isinstance(value, int): return 'int'
    if isinstance(value, float): return 'float'
    if isinstance(value, str): return 'string'
    if isinstance(value, list): return 'array'
    if isinstance(value, set): return 'set'
    if isinstance(value, bool): return 'bool'
    warn(f'{value} TYPE NOT RECOG'); return 'int'
def string(value):
    value_type = type_(value)
    if value_type == 'int': return str(value)
    if value_type == 'float': return str(value)
    if value_type == 'string': return "'"+value if len(value)==1 else '"'+value+'"'
    if value_type == 'bool':
        if value: return 'y'
        return 'n'
    if value_type == 'list': return '['+','.join(string(i) for i in value)+']'
    if value_type == 'set': return '{'+','.join(string(i) for i in value)+'}'
    warn(f'{value} STR NOT RECOG AT LINE {current_line+1}'); return '0'
def implied_type_conversion(value, to_type, implied=True):
    from_type = type_(value)
    if type(to_type) == dict: to_type = to_type[from_type]
    if from_type == to_type: return value
    if implied: warn(f'IMPL TYPE CONV AT LINE {current_line+1}')
    if from_type == 'int' and to_type == 'float': return float(value)
    if from_type == 'float' and to_type == 'int': return int(value//1)
    if from_type == 'string' and to_type == 'character': return value[0]
    if from_type == 'array' and to_type == 'set': return set(value)
    if from_type == 'set' and to_type == 'array': return sorted(list(value))
    if from_type == 'set' and to_type == 'stack':
        stack = list(value)
        random.shuffle(stack)
        return stack
    if from_type == 'int' and to_type == 'bool': return value!=0
    if from_type == 'float' and to_type == 'bool': return value>0
    if from_type == 'bool' and to_type == 'int': return int(value)
    if from_type == 'bool' and to_type == 'float': return float(int(value))
    if from_type == 'string' and to_type == 'array': return list(value)
    if from_type == 'string' and to_type == 'set': return set(value)
    if from_type == 'string' and to_type == 'stack': return list(value)
    if to_type == 'string': return string(value)
    if from_type == 'array' and to_type == 'character': return '['
    if from_type == 'set' and to_type == 'character': return '{'
    if from_type == 'float' and to_type == 'character':
        if value > 0: return '+'
        if value < 0: return '-'
        return '0'
    if from_type == 'int' and to_type == 'character':
        if value > 0: return '+'
        if value < 0: return '-'
        return '0'
    if from_type == 'bool' and to_type == 'character':
        if value: return 'y'
        return 'n'
    if from_type == 'array' and to_type == 'bool': return value==[]
    if from_type == 'set' and to_type == 'bool': return value==set()
    if from_type == 'stack' and to_type == 'bool': return value==[]
    if from_type == 'bool' and to_type == 'array': return []
    if from_type == 'bool' and to_type == 'set': return set()
    if from_type == 'bool' and to_type == 'stack': return []
    if from_type == 'string' and to_type == 'bool': return value==''
    if from_type == 'string' and to_type == 'int': return len(value)
    if from_type == 'string' and to_type == 'float': return float(len(value))
    if from_type == 'int' and to_type == 'array': return [*range(1,value+1)]
    if from_type == 'int' and to_type == 'set': return set(range(1,value+1))
    if from_type == 'int' and to_type == 'stack': return [*range(1,value+1)]
    if from_type == 'float' and to_type == 'array': return [*range(1,(value//1)+1)]
    if from_type == 'float' and to_type == 'set': return set(range(1,(value//1)+1))
    if from_type == 'float' and to_type == 'stack': return [*range(1,(value//1)+1)]
    if from_type == 'array' and to_type == 'int': return len(value)
    if from_type == 'set' and to_type == 'int': return len(value)
    if from_type == 'array' and to_type == 'float': return float(len(value))
    if from_type == 'set' and to_type == 'float': return float(len(value))
    warn(f'UNEXP ERR AT LINE {current_line+1}')

def less(a, b):
    if type_(a) == 'int': return a < implied_type_conversion(b, 'int')
    if type_(a) == 'float': return a < implied_type_conversion(b, 'float')
    if type_(a) == 'string': return a < implied_type_conversion(b, 'string')
    if type_(a) == 'bool': return a < implied_type_conversion(b, 'bool')
    if type_(a) == 'array':
        b = implied_type_conversion(b, 'array')
        for i in range(min(len(a), len(b))):
            if less(a[i], b[i]): return True
            if less(b[i], a[i]): return False
        return len(a) < len(b)
    if type_(a) == 'set':
        b = implied_type_conversion(b, 'set')
        if len(a) >= len(b): return False
        for i in a:
            if i not in b: return False
        return True
def greater(a, b): return less(b, a)
def equal(a, b):
    if type_(a) == 'int': return a == implied_type_conversion(b, 'int')
    if type_(a) == 'float': return a == implied_type_conversion(b, 'float')
    if type_(a) == 'string': return a == implied_type_conversion(b, 'string')
    if type_(a) == 'bool': return a == implied_type_conversion(b, 'bool')
    if type_(a) == 'array':
        b = implied_type_conversion(b, 'array')
        return a==b
    if type_(a) == 'set':
        b = implied_type_conversion(b, 'set')
        return implied_type_conversion(a, 'array', implied=False) == \
               implied_type_conversion(b, 'array', implied=False)

def report():
    if debug_mode or verbose_mode:
        print(f'\nCurrent Line: {current_line}')
        print(f'\nInstruction: {instruction}')
        print(f'\nParameters: {parameters}')
        print(f'\nVariables: {variables}')
        print()
def warn(message):
    if not disable_warnings:
        # use red color for warnings
        print(f'\n\033[91mWARNING: {message}\033[0m\n')

try:
    while current_line < len(program):
        instruction = program[current_line][0]
        parameters = program[current_line][1]
        report()

        if False: pass
        elif instruction == '': pass
        elif instruction == 'comment': pass
        elif instruction == 'in':
            if parameters == '':
                if 'last' in variables:
                    variables['last'] = input(implied_type_conversion(variables['last'], 'string'))
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    variables['last'] = input(implied_type_conversion(variables['last'], 'string'))
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    variables['last'] = input(implied_type_conversion(variables[var_name], 'string'))
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    variables['last'] = input(implied_type_conversion(variables[var_name], 'string'))
        elif instruction == 'out':
            if parameters == '':
                if 'last' in variables:
                    print(implied_type_conversion(variables['last'], 'string'))
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    print(implied_type_conversion(variables['last'], 'string'))
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    print(implied_type_conversion(variables[var_name], 'string'))
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    print(implied_type_conversion(variables[var_name], 'string'))
        elif instruction == 'line':
            if parameters == '':
                if 'last' in variables:
                    print(implied_type_conversion(variables['last'], 'string'), end='')
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    print(implied_type_conversion(variables['last'], 'string'), end='')
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    print(implied_type_conversion(variables[var_name], 'string'), end='')
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    print(implied_type_conversion(variables[var_name], 'string'), end='')
        elif instruction == 'set':
            parameters = ' '+parameters+' '
            if ' to ' in parameters:
                var_name, var_value = parameters.split(' to ')
                var_name, var_value = var_name.strip(), var_value.strip()
                if var_name == '': var_name = 'last'
                if var_value == '':
                    if 'last' in variables:
                        var_value = 'last'
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        var_value = 'last'
                if var_value == 'last': var_value = variables['last']
                else: var_value = parse_value(var_value)
                variables[var_name] = var_value
                variables['last'] = var_value
            else:
                warn(f'UNEXP LINE {current_line+1}')
        elif instruction == 'skip':
            if parameters == '':
                if 'last' in variables:
                    current_line += implied_type_conversion(variables['last'], 'int')
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    current_line += implied_type_conversion(variables['last'], 'int')
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    current_line += implied_type_conversion(variables[var_name], 'int')
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    current_line += implied_type_conversion(variables[var_name], 'int')
        elif instruction == 'back':
            if parameters == '':
                if 'last' in variables:
                    current_line -= implied_type_conversion(variables['last'], 'int')+1
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    current_line -= implied_type_conversion(variables['last'], 'int')+1
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    current_line -= implied_type_conversion(variables[var_name], 'int')+1
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    current_line -= implied_type_conversion(variables[var_name], 'int')+1
        elif instruction == 'goto':
            if parameters == '':
                if 'last' in variables:
                    current_line = implied_type_conversion(variables['last'], 'int')-1
                else:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                    current_line = implied_type_conversion(variables['last'], 'int')-1
            else:
                var_name = parameters.strip()
                if var_name in variables:
                    current_line = implied_type_conversion(variables[var_name], 'int')-1
                else:
                    warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                    variables[var_name] = 0
                    current_line = implied_type_conversion(variables[var_name], 'int')-1
        elif instruction == 'exit': break
        elif instruction == 'calc':
            function, *arguments = parameters.split(' ')
            arguments = [*arguments]
            if False: pass
            elif function == 'addition':
                if all([type_(argument,1)=='int' for argument in arguments]):
                    sum = 0
                    for argument in arguments:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum += implied_type_conversion(variables[argument], 'int')
                    variables['last'] = sum
                else:
                    sum = 0.0
                    for argument in arguments:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum += implied_type_conversion(variables[argument], 'float')
                    variables['last'] = sum
            elif function == 'subtraction':
                if all([type_(argument,1)=='int' for argument in arguments]):
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'int')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum -= implied_type_conversion(variables[argument], 'int')
                    variables['last'] = sum
                else:
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'float')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum -= implied_type_conversion(variables[argument], 'float')
                    variables['last'] = sum
            elif function == 'multiplication':
                if all([type_(argument,1)=='int' for argument in arguments]):
                    sum = 1
                    for argument in arguments:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum *= implied_type_conversion(variables[argument], 'int')
                    variables['last'] = sum
                else:
                    sum = 1.0
                    for argument in arguments:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum *= implied_type_conversion(variables[argument], 'float')
                    variables['last'] = sum
            elif function == 'division':
                if any([argument not in variables or
                        variables[argument]==0 for argument in arguments[1:]]):
                    warn(f'DIV BY ZERO IN LINE {current_line+1}')
                    variables['last'] = 0
                elif all([type_(argument,1)=='int' for argument in arguments]):
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'int')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum /= implied_type_conversion(variables[argument], 'int')
                    variables['last'] = sum
                else:
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'float')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum /= implied_type_conversion(variables[argument], 'float')
                    variables['last'] = sum
            elif function == 'modulo':
                if any([argument in variables or
                        variables[argument]==0 for argument in arguments]):
                    warn(f'DIV BY ZERO IN LINE {current_line+1}')
                    variables['last'] = 0
                elif all([type_(argument,1)=='int' for argument in arguments]):
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'int')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum %= implied_type_conversion(variables[argument], 'int')
                    variables['last'] = sum
                else:
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    sum = implied_type_conversion(variables[arguments[0]], 'float')
                    for argument in arguments[1:]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        sum %= implied_type_conversion(variables[argument], 'float')
                    variables['last'] = sum
            elif function == 'power':
                if all([type_(argument,1)=='int' for argument in arguments]):
                    if arguments[-1] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[-1]] = 0
                    sum = implied_type_conversion(variables[arguments[-1]], 'int')
                    for argument in arguments[-1:0:-1]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        if sum==implied_type_conversion(variables[argument], 'int')==0:
                            warn(f'ZERO POW ZERO IN LINE {current_line+1}')
                            sum=1
                            continue
                        try: sum = implied_type_conversion(variables[argument], 'int') ** sum
                        except ZeroDivisionError:
                            warn(f'DIV BY ZERO IN LINE {current_line+1}')
                            sum = 0
                    variables['last'] = sum
                else:
                    if arguments[-1] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[-1]] = 0
                    sum = implied_type_conversion(variables[arguments[-1]], 'float')
                    for argument in arguments[:-1]:
                        if argument not in variables:
                            warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                            variables[argument] = 0
                        if sum==implied_type_conversion(variables[argument], 'float')==0:
                            warn(f'ZERO POW ZERO IN LINE {current_line+1}')
                            variables['last'] = 1
                        try: sum = implied_type_conversion(variables[argument], 'float') ** sum
                        except ZeroDivisionError:
                            warn(f'DIV BY ZERO IN LINE {current_line+1}')
                            sum = 0
                    variables['last'] = sum
            elif function == 'less':
                true = True
                for i in range(len(arguments)-1):
                    if arguments[i] not in variables:
                        warn(f'UNDEF VAR {arguments[i]} IN LINE {current_line+1}')
                        variables[arguments[i]] = 0
                    if arguments[i+1] not in variables:
                        warn(f'UNDEF VAR {arguments[i+1]} IN LINE {current_line+1}')
                        variables[arguments[i+1]] = 0
                    true = true and less(variables[arguments[i]], variables[arguments[i+1]])
                variables['last'] = true
            elif function == 'greater':
                true = True
                for i in range(len(arguments)-1):
                    if arguments[i] not in variables:
                        warn(f'UNDEF VAR {arguments[i]} IN LINE {current_line+1}')
                        variables[arguments[i]] = 0
                    if arguments[i+1] not in variables:
                        warn(f'UNDEF VAR {arguments[i+1]} IN LINE {current_line+1}')
                        variables[arguments[i+1]] = 0
                    true = true and greater(variables[arguments[i]], variables[arguments[i+1]])
                variables['last'] = true
            elif function == 'equal':
                true = True
                for i in range(len(arguments)-1):
                    if arguments[i] not in variables:
                        warn(f'UNDEF VAR {arguments[i]} IN LINE {current_line+1}')
                        variables[arguments[i]] = 0
                    if arguments[i+1] not in variables:
                        warn(f'UNDEF VAR {arguments[i+1]} IN LINE {current_line+1}')
                        variables[arguments[i+1]] = 0
                    true = true and equal(variables[arguments[i]], variables[arguments[i+1]])
                variables['last'] = true
            elif function == 'pop':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                try: variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                            'array')[1:]
                except IndexError:
                    warn(f'POP FROM EMPT ARR IN LINE {current_line+1}')
                    variables['last'] = 0
            elif function == 'reverse':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                            'array')[::-1]
            elif function == 'index':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                try: variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                            'array')[implied_type_conversion(
                    variables[arguments[1]],
                    'int')]
                except IndexError:
                    warn(f'INDEX OUT OF RANGE IN LINE {current_line+1}')
                    variables['last'] = 0
            elif function == 'push':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                            'array') + [variables[arguments[1]]]
            elif function == 'join':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = \
                implied_type_conversion(variables[arguments[1]],
                    'string').join([implied_type_conversion(i,
                    'string') for i in implied_type_conversion(
                    variables[arguments[0]], 'array')])
            elif function == 'split':
                arguments += ['last']*5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = implied_type_conversion(variables[arguments[0]],
                    'string').split(implied_type_conversion(variables[arguments[1]],
                    'string'))
            elif function == 'range':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                if arguments[2] not in variables:
                    warn(f'UNDEF VAR {arguments[2]} IN LINE {current_line+1}')
                    variables[arguments[2]] = 0
                range_ = []
                _1, _2, _3 = implied_type_conversion(variables[arguments[0]],
                                                     'float'), \
                            implied_type_conversion(variables[arguments[1]],
                                                     'float'), \
                            implied_type_conversion(variables[arguments[2]],
                                                     'float')
                while True:
                    if _1 > _3:
                        break
                    range_.append(_1)
                    _1 += _2
                variables['last'] = range_
            elif function == 'type':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = implied_type_conversion(variables[arguments[0]],
                    type_(variables[arguments[1]]), implied=False)
            elif function == 'int':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = int(implied_type_conversion(
                    variables[arguments[0]],
                    'string'))
            elif function == 'float':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = float(implied_type_conversion(
                    variables[arguments[0]],
                    'string'))
            # math functions
            elif function == 'sine':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.sin(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'cosine':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.cos(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'tangent':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.tan(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'arcsine':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.asin(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'arccosine':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.acos(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'arctangent':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.atan(implied_type_conversion(
                    variables[arguments[0]],
                    'float'))
            elif function == 'phi': variables['last'] = (5**0.5+1)/2
            elif function == 'pi': variables['last'] = math.pi
            elif function == 'e': variables['last'] = math.e
            elif function == 'factorial':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                variables['last'] = math.factorial(implied_type_conversion(
                    variables[arguments[0]],
                    'int'))
            elif function == 'log':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = math.log(implied_type_conversion(
                    variables[arguments[0]],
                    'float'), implied_type_conversion(variables[arguments[1]],
                    'float'))
            # set functions
            elif function == 'union':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = set(implied_type_conversion(
                    variables[arguments[0]],
                    'list')) | set(implied_type_conversion(
                    variables[arguments[1]],
                    'list'))
            elif function == 'intersection':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = set(implied_type_conversion(
                    variables[arguments[0]],
                    'list')) & set(implied_type_conversion(
                    variables[arguments[1]],
                    'list'))
            elif function == 'difference':
                arguments += ['last'] * 5
                if arguments[0] not in variables:
                    warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                    variables[arguments[0]] = 0
                if arguments[1] not in variables:
                    warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                    variables[arguments[1]] = 0
                variables['last'] = set(implied_type_conversion(
                    variables[arguments[0]],
                    'list')) - set(implied_type_conversion(
                    variables[arguments[1]],
                    'list'))
        else: warn(f'UNEXP LINE {current_line+1}')
        current_line += 1
except Exception as e:
    warn(f'UNEXP ERR IN LINE {current_line+1}')
    if debug_mode: warn(f'The exception raised was:\n\n\n{e}'); raise
    exit()

if debug_mode or verbose_mode: print('\n')

# By the way, nobody is looking at the source code, right?