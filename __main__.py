# SLWNSNBP, or "Sun Sip"
# Simple Language Whose Name Should Not Be Pronounced

import random
import math
import sys
import os
import re

def before_run():

    if not '-n' in sys.argv: print('\n'*1000)
    if '--help' in sys.argv: print('''
    Syntax: python3 main.py program.slwnsnbp [options]
    Options:
        --help   : Print this help message and exit.
        -d       : Debug mode.
        -w       : Disable warnings.
        -n       : Disable newlines added in front.
        -e       : All errors fail silently.
        --syntax : Syntax highlight the source code and exit.
        -r       : Use rich printing, see the rich module.
    '''); sys.exit()

    if '-v' in sys.argv:
        print('''\033[91mVerbose Mode is not supported since 2.0.0\033[0m\n''')

    try:
        file_containing_program = sys.argv[1]
    except IndexError:
        print('\033[91m\nNo program specified.\n'
              'Use the --help option for '
              'usage help.\033[0m\n'); sys.exit()
    debug_mode = '-d' in sys.argv
    disable_warnings = '-w' in sys.argv
    verbose_mode = False
    noerr_mode = '-e' in sys.argv

    try:
        with open(file_containing_program, 'r') as f:
            program = f.readlines()
    except FileNotFoundError:
        print(f'\033[91mSorry, I can not find the file: '
              f'{file_containing_program}.'
              f'\nCheck the path, name, and file extension.'
              f'\nFor usage help, use the --help option.\033[0m\n')
        sys.exit()

    if '--syntax' in sys.argv:
        program = '\n'.join(program)

        # Simple Syntax Highlighter for SunSip

        try: import rich
        except ImportError:
            print('''\033[91mThe module "rich" needs to be installed.\033[0m\n''')
        from rich.markup import escape as textize

        def syntax_highlight(text):
            text = textize(text)
            output = ''
            lines = text.split('\n')
            for line in lines:
                while line.startswith(' '):
                    output += '[on red] [default on default]'
                    line = line[1:]
                if line == '':
                    output += '[default on default]\n'
                    continue
                command, *_ = line.split(' ')
                if not _:
                    if command == 'comment':
                        output += '[#333333]comment'
                        output += '[default on default]\n'
                    elif command in ['in', 'out', 'line']:
                        output += f'[#44ff00]{command}'
                        output += '[default on default]\n'
                    elif command in ['skip', 'back', 'goto', 'exit', 'recurse', 'defined']:
                        output += f'[#998800]{command}'
                        output += '[default on default]\n'
                    else:
                        output += f'[#ff0000]{command}'
                        output += '[default on default]\n'

                else:
                    if command == 'comment':
                        output += f'[#333333]{line}'
                        output += '[default on default]\n'
                    elif command in ['in', 'out', 'line']:
                        if len(_) == 1:
                            output += f'[#44ff00]{command} {_[0]}'
                            output += '[default on default]\n'
                        else:
                            output += f'[#44ff00]{command} {_[0]}[#333333] {" ".join(_[1:])}'
                            output += '[default on default]\n'
                    elif command in ['skip', 'back', 'goto', 'defined']:
                        if len(_) == 1:
                            output += f'[#998800]{command} {_[0]}'
                            output += '[default on default]\n'
                        else:
                            output += f'[#998800]{command} {_[0]}[#333333] {" ".join(_[1:])}'
                            output += '[default on default]\n'
                    elif command in ['exit','recurse']:
                        output += f'[#998800]{command}[#333333] {" ".join(_)}'
                        output += '[default on default]\n'
                    elif command == 'set':
                        arguments = ' '.join(_)
                        if arguments.strip() == 'to':
                            output += f'[#333333]{line}'
                            output += '[default on default]\n'
                        elif arguments.strip().startswith('to '):
                            output += f'[#4400ff]{command} ' \
                                      f'[#ffaadd]{arguments.split("to ", 1)[0]}to ' \
                                      f'[#{parse(arguments.split("to ", 1)[1])}]' \
                                      f'{arguments.split("to ", 1)[1]}'
                            output += '[default on default]\n'
                        elif arguments.strip().endswith(' to'):
                            output += f'[#4400ff]{command} ' \
                                      f'[#3388cc]{arguments.rsplit(" to", 1)[0]} ' \
                                      f'[#ffaadd]to{arguments.rsplit(" to", 1)[1]}'
                            output += '[default on default]\n'
                        elif ' to ' in f' {arguments} ':
                            output += f'[#4400ff]{command} ' \
                                      f'[#3388cc]{arguments.split(" to ", 1)[0]} ' \
                                      f'[#ffaadd]to ' \
                                      f'[#{parse(arguments.split(" to ", 1)[1])}]' \
                                      f'{arguments.split(" to ", 1)[1]}'
                            output += '[default on default]\n'
                        else:
                            output += f'[#ff0000]{line}'
                            output += '[default on default]\n'
                    elif command == 'calc':
                        if len(_) == 1:
                            output += f'[#4400ff]{command} [#3388cc]{_[0]}'
                            output += '[default on default]\n'
                        else:
                            output += f'[#4400ff]{command} [#3388cc]{_[0]} ' \
                                      f'[#ff00ff]{" ".join(_[1:])}'
                            output += '[default on default]\n'

            return output

        def get_value(value_as_string):

            value = value_as_string

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

            return None

        def type_(value):
            if isinstance(value, bool): return 'bool'
            if isinstance(value, int): return 'int'
            if isinstance(value, float): return 'float'
            if isinstance(value, str): return 'string'
            if isinstance(value, list): return 'array'
            if isinstance(value, set): return 'set'
            return 'none'

        def parse(value):
            value = value.strip()
            if value == 'last': return '002288'
            if value == 'y': return '006600'
            if value == 'n': return '660000'
            typ = type_(get_value(value))
            dictionary = {
                'int': 'cc4400',
                'float': 'cc4400',
                'string': '446600',
                'array': '222288',
                'set': '222288',
                'none': 'ff0000',
            }
            return dictionary[typ]

        def main():
            print('\n' * 1000)
            if '--help' in sys.argv: print('''
            Syntax: python3 syntax.py program.slwnsnbp [options]
            Options:
                --help : Print this help message and exit.
            '''); sys.exit()

            try:
                file_containing_program = sys.argv[1]
            except IndexError:
                print('\033[91m\nNo program specified.\n'
                      'Use the --help option for '
                      'usage help.\033[0m\n');
                sys.exit()

            try:
                with open(file_containing_program, 'r') as f:
                    program = f.read()
            except FileNotFoundError:
                print(f'\033[91mSorry, I can not find the file: '
                      f'{file_containing_program}.'
                      f'\nCheck the path, name, and file extension.'
                      f'\nFor usage help, use the --help option.\033[0m\n')
                sys.exit()

            rich.print(syntax_highlight(program))

        main()

        exit()

    use_rich = '-r' in sys.argv

    return program, debug_mode, disable_warnings, use_rich

program, debug_mode, disable_warnings, use_rich = before_run()

if use_rich:
    try: from rich import print
    except ImportError:
        print('''\033[91mThe module "rich" needs to be installed.\n''' \
              '''Alternatively, omit the '-r' flag.\033[0m\n''')

def parse_program(program):
    program = [i.strip() for i in program]
    program = [[i.split(' ')[0], ' '.join(i.split(' ')[1:])] for i in program]
    program = [[j.strip() for j in i] for i in program]
    return program
program = parse_program(program)
if debug_mode: print(f'\nProgram:\n{program}\n')

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
def type_(value, careful=0, variables={}):
    if careful: return 'int' if value not in variables else type_(variables[value])
    if isinstance(value, bool): return 'bool'
    if isinstance(value, int): return 'int'
    if isinstance(value, float): return 'float'
    if isinstance(value, str): return 'string'
    if isinstance(value, list): return 'array'
    if isinstance(value, set): return 'set'
    warn(f'{value} TYPE NOT RECOG'); return 'int'
def string(value):
    value_type = type_(value)
    if value_type == 'int': return str(value)
    if value_type == 'float': return str(value)
    if value_type == 'string': return "'"+value if len(value)==1 else '"'+value+'"'
    if value_type == 'bool':
        if value: return 'y'
        return 'n'
    if value_type == 'array': return '['+','.join(string(i) for i in value)+']'
    if value_type == 'set': return '{'+','.join(string(i) for i in value)+'}'
    warn(f'{value} STR NOT RECOG AT LINE {current_line+1}'); return '0'
def implied_type_conversion(value, to_type, current_line, implied=True):
    from_type = type_(value)
    if type(to_type) == dict: to_type = to_type[from_type]
    if from_type == to_type: return value
    if implied: warn(f'IMPL TYPE CONV AT LINE {current_line+1}')
    if from_type == 'int' and to_type == 'float': return float(value)
    if from_type == 'float' and to_type == 'int': return int(value//1)
    if from_type == 'string' and to_type == 'character': return value[0]
    if from_type == 'array' and to_type == 'set': return set(value)
    if from_type == 'set' and to_type == 'array': return sorted(list(value))
    if from_type == 'array' and to_type == 'stack': return value
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
    if from_type == 'array' and to_type == 'bool': return value!=[]
    if from_type == 'set' and to_type == 'bool': return value!=set()
    if from_type == 'stack' and to_type == 'bool': return value!=[]
    if from_type == 'bool' and to_type == 'array': return []
    if from_type == 'bool' and to_type == 'set': return set()
    if from_type == 'bool' and to_type == 'stack': return []
    if from_type == 'string' and to_type == 'bool': return value!=''
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

def less(a, b, current_line):
    if type_(a) == 'int': return a < implied_type_conversion(b, 'int', current_line)
    if type_(a) == 'float': return a < implied_type_conversion(b, 'float', current_line)
    if type_(a) == 'string': return a < implied_type_conversion(b, 'string', current_line)
    if type_(a) == 'bool': return a < implied_type_conversion(b, 'bool', current_line)
    if type_(a) == 'array':
        b = implied_type_conversion(b, 'array', current_line)
        for i in range(min(len(a), len(b))):
            if less(a[i], b[i], current_line): return True
            if less(b[i], a[i], current_line): return False
        return len(a) < len(b)
    if type_(a) == 'set':
        b = implied_type_conversion(b, 'set', current_line)
        if len(a) >= len(b): return False
        for i in a:
            if i not in b: return False
        return True
def greater(a, b, current_line): return less(b, a, current_line)
def equal(a, b, current_line):
    if type_(a) == 'int': return a == implied_type_conversion(b, 'int', current_line)
    if type_(a) == 'float': return a == implied_type_conversion(b, 'float', current_line)
    if type_(a) == 'string': return a == implied_type_conversion(b, 'string', current_line)
    if type_(a) == 'bool': return a == implied_type_conversion(b, 'bool', current_line)
    if type_(a) == 'array':
        b = implied_type_conversion(b, 'array', current_line)
        return a==b
    if type_(a) == 'set':
        b = implied_type_conversion(b, 'set', current_line)
        return implied_type_conversion(a, 'array', current_line, implied=False) == \
               implied_type_conversion(b, 'array', current_line, implied=False)

def report(current_line, instruction, parameters, variables):
    if debug_mode:
        print(f'\nCurrent Line: {current_line}')
        print(f'\nInstruction: {instruction}')
        print(f'\nParameters: {parameters}')
        print(f'\nVariables: {variables}')
        print()
def warn(message):
    if not disable_warnings:
        # use red color for warnings
        print(f'\n\033[91mWARNING: {message}\033[0m\n')

def run(program, variables = None):
    if variables == None: variables = {}
    current_line = 0
    try:
        while -1 < current_line < len(program):
            instruction = program[current_line][0]
            parameters = program[current_line][1]
            report(current_line, instruction, parameters, variables)

            if False: pass
            elif instruction == '': pass
            elif instruction == 'comment': pass
            elif instruction == 'in':
                if parameters == '':
                    if 'last' in variables:
                        variables['last'] = input(implied_type_conversion(variables['last'], 'string', current_line))
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        variables['last'] = input(implied_type_conversion(variables['last'], 'string', current_line))
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        variables['last'] = input(implied_type_conversion(variables[var_name], 'string', current_line))
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        variables['last'] = input(implied_type_conversion(variables[var_name], 'string', current_line))
            elif instruction == 'out':
                if parameters == '':
                    if 'last' in variables:
                        print(implied_type_conversion(variables['last'], 'string', current_line))
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        print(implied_type_conversion(variables['last'], 'string', current_line))
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        print(implied_type_conversion(variables[var_name], 'string', current_line))
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        print(implied_type_conversion(variables[var_name], 'string', current_line))
            elif instruction == 'line':
                if parameters == '':
                    if 'last' in variables:
                        print(implied_type_conversion(variables['last'], 'string', current_line), end='')
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        print(implied_type_conversion(variables['last'], 'string', current_line), end='')
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        print(implied_type_conversion(variables[var_name], 'string', current_line), end='')
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        print(implied_type_conversion(variables[var_name], 'string', current_line), end='')
            elif instruction == 'set':
                parameters = ' '+parameters+' '
                if ' to ' in parameters:
                    var_name, var_value = parameters.split(' to ')
                    var_name, var_value = var_name.strip(), var_value.strip()
                    if var_name == '': var_name = 'last'
                    if var_value == '':
                        if 'last' in variables: var_value = 'last'
                        else: var_value = None
                    if var_value == 'last': var_value = variables['last']
                    elif var_value != None: var_value = parse_value(var_value)
                    if var_value != None: variables[var_name] = var_value
                else:
                    warn(f'UNEXP LINE {current_line+1}')
            elif instruction == 'skip':
                if parameters == '':
                    if 'last' in variables:
                        current_line += implied_type_conversion(variables['last'], 'int', current_line)
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        current_line += implied_type_conversion(variables['last'], 'int', current_line)
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        current_line += implied_type_conversion(variables[var_name], 'int', current_line)
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        current_line += implied_type_conversion(variables[var_name], 'int', current_line)
            elif instruction == 'back':
                if parameters == '':
                    if 'last' in variables:
                        current_line -= implied_type_conversion(variables['last'], 'int', current_line)+1
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        current_line -= implied_type_conversion(variables['last'], 'int', current_line)+1
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        current_line -= implied_type_conversion(variables[var_name], 'int', current_line)+1
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        current_line -= implied_type_conversion(variables[var_name], 'int', current_line)+1
            elif instruction == 'goto':
                if parameters == '':
                    if 'last' in variables:
                        current_line = implied_type_conversion(variables['last'], 'int', current_line)-1
                    else:
                        warn(f'UNDEF VAR last IN LINE {current_line}')
                        variables['last'] = 0
                        current_line = implied_type_conversion(variables['last'], 'int', current_line)-1
                else:
                    var_name = parameters.strip()
                    if var_name in variables:
                        current_line = implied_type_conversion(variables[var_name], 'int', current_line)-1
                    else:
                        warn(f'UNDEF VAR {var_name} IN LINE {current_line}')
                        variables[var_name] = 0
                        current_line = implied_type_conversion(variables[var_name], 'int', current_line)-1
            elif instruction == 'exit': break
            elif instruction == 'calc':
                function, *arguments = parameters.split(' ')
                arguments = [*arguments]
                if False: pass
                elif function == 'addition':
                    if all([type_(argument,1,variables)=='int' for argument in arguments]):
                        sum = 0
                        for argument in arguments:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum += implied_type_conversion(variables[argument], 'int', current_line)
                        variables['last'] = sum
                    else:
                        sum = 0.0
                        for argument in arguments:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum += implied_type_conversion(variables[argument], 'float', current_line)
                        variables['last'] = sum
                elif function == 'subtraction':
                    if all([type_(argument,1,variables)=='int' for argument in arguments]):
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'int', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum -= implied_type_conversion(variables[argument], 'int', current_line)
                        variables['last'] = sum
                    else:
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'float', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum -= implied_type_conversion(variables[argument], 'float', current_line)
                        variables['last'] = sum
                elif function == 'multiplication':
                    if all([type_(argument,1,variables)=='int' for argument in arguments]):
                        sum = 1
                        for argument in arguments:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum *= implied_type_conversion(variables[argument], 'int', current_line)
                        variables['last'] = sum
                    else:
                        sum = 1.0
                        for argument in arguments:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum *= implied_type_conversion(variables[argument], 'float', current_line)
                        variables['last'] = sum
                elif function == 'division':
                    if any([argument not in variables or
                            variables[argument]==0 for argument in arguments[1:]]):
                        warn(f'DIV BY ZERO IN LINE {current_line+1}')
                        variables['last'] = 0
                    elif all([type_(argument,1,variables)=='int' for argument in arguments]):
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'int', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum /= implied_type_conversion(variables[argument], 'int', current_line)
                        variables['last'] = sum
                    else:
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'float', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum /= implied_type_conversion(variables[argument], 'float', current_line)
                        variables['last'] = sum
                elif function == 'modulo':
                    if any([argument in variables or
                            variables[argument]==0 for argument in arguments]):
                        warn(f'DIV BY ZERO IN LINE {current_line+1}')
                        variables['last'] = 0
                    elif all([type_(argument,1,variables)=='int' for argument in arguments]):
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'int', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum %= implied_type_conversion(variables[argument], 'int', current_line)
                        variables['last'] = sum
                    else:
                        if arguments[0] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[0]] = 0
                        sum = implied_type_conversion(variables[arguments[0]], 'float', current_line)
                        for argument in arguments[1:]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            sum %= implied_type_conversion(variables[argument], 'float', current_line)
                        variables['last'] = sum
                elif function == 'power':
                    if all([type_(argument,1,variables)=='int' for argument in arguments]):
                        if arguments[-1] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[-1]] = 0
                        sum = implied_type_conversion(variables[arguments[-1]], 'int', current_line)
                        for argument in arguments[-1:0:-1]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            if sum==implied_type_conversion(variables[argument], 'int', current_line)==0:
                                warn(f'ZERO POW ZERO IN LINE {current_line+1}')
                                sum=1
                                continue
                            try: sum = implied_type_conversion(variables[argument], 'int', current_line) ** sum
                            except ZeroDivisionError:
                                warn(f'DIV BY ZERO IN LINE {current_line+1}')
                                sum = 0
                        variables['last'] = sum
                    else:
                        if arguments[-1] not in variables:
                            warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                            variables[arguments[-1]] = 0
                        sum = implied_type_conversion(variables[arguments[-1]], 'float', current_line)
                        for argument in arguments[:-1]:
                            if argument not in variables:
                                warn(f'UNDEF VAR {argument} IN LINE {current_line+1}')
                                variables[argument] = 0
                            if sum==implied_type_conversion(variables[argument], 'float', current_line)==0:
                                warn(f'ZERO POW ZERO IN LINE {current_line+1}')
                                variables['last'] = 1
                            try: sum = implied_type_conversion(variables[argument], 'float', current_line) ** sum
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
                        true = true and less(variables[arguments[i]], variables[arguments[i+1]], current_line)
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
                        true = true and greater(variables[arguments[i]], variables[arguments[i+1]], current_line)
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
                    variables['last'] = True
                elif function == 'pop':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    try: variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                                'array', current_line)[1:]
                    except IndexError:
                        warn(f'POP FROM EMPT ARR IN LINE {current_line+1}')
                        variables['last'] = 0
                elif function == 'reverse':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                                'array', current_line)[::-1]
                elif function == 'index':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    if arguments[1] not in variables:
                        warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                        variables[arguments[1]] = 0
                    try: variables['last'] = implied_type_conversion(variables[arguments[0]],
                                                                'array', current_line)[implied_type_conversion(
                        variables[arguments[1]],
                        'int', current_line)]
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
                                                                'array', current_line) + [variables[arguments[1]]]
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
                        'string', current_line).join([implied_type_conversion(i,
                        'string', current_line) for i in implied_type_conversion(
                        variables[arguments[0]], 'array', current_line)])
                elif function == 'split':
                    arguments += ['last']*5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    if arguments[1] not in variables:
                        warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                        variables[arguments[1]] = 0
                    variables['last'] = implied_type_conversion(variables[arguments[0]],
                        'string', current_line).split(implied_type_conversion(variables[arguments[1]],
                        'string', current_line))
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
                                                         'float', current_line), \
                                implied_type_conversion(variables[arguments[1]],
                                                         'float', current_line), \
                                implied_type_conversion(variables[arguments[2]],
                                                         'float', current_line)
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
                        type_(variables[arguments[1]]), current_line, implied=False)
                elif function == 'verbatimtype':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    if arguments[1] not in variables:
                        warn(f'UNDEF VAR {arguments[1]} IN LINE {current_line+1}')
                        variables[arguments[1]] = 0
                    variables['last'] = implied_type_conversion(variables[arguments[0]],
                        variables[arguments[1]], current_line, implied=False)
                elif function == 'int':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = int(implied_type_conversion(
                        variables[arguments[0]],
                        'string', current_line))
                elif function == 'float':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = float(implied_type_conversion(
                        variables[arguments[0]],
                        'string', current_line))
                elif function == 'character':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = chr(implied_type_conversion(
                        variables[arguments[0]],
                        'int', current_line))
                elif function == 'ordinal':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = ord(implied_type_conversion(
                        variables[arguments[0]],
                        'character', current_line))
                # math functions
                elif function == 'sine':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.sin(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
                elif function == 'cosine':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.cos(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
                elif function == 'tangent':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.tan(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
                elif function == 'arcsine':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.asin(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
                elif function == 'arccosine':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.acos(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
                elif function == 'arctangent':
                    arguments += ['last'] * 5
                    if arguments[0] not in variables:
                        warn(f'UNDEF VAR {arguments[0]} IN LINE {current_line+1}')
                        variables[arguments[0]] = 0
                    variables['last'] = math.atan(implied_type_conversion(
                        variables[arguments[0]],
                        'float', current_line))
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
                        'int', current_line))
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
                        'float', current_line), implied_type_conversion(variables[arguments[1]],
                        'float', current_line))
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
                        'list', current_line)) | set(implied_type_conversion(
                        variables[arguments[1]],
                        'list', current_line))
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
                        'list', current_line)) & set(implied_type_conversion(
                        variables[arguments[1]],
                        'list', current_line))
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
                        'list', current_line)) - set(implied_type_conversion(
                        variables[arguments[1]],
                        'list', current_line))
            elif instruction == 'recurse':
                if 'last' not in variables:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    variables['last'] = 0
                vars = run(program, {'last': variables['last']})
                if 'last' not in vars:
                    warn(f'UNDEF VAR last IN LINE {current_line}')
                    vars['last'] = 0
                variables['last'] = vars['last']
            elif instruction == 'defined':
                if parameters == '':
                    variables['last'] = 'last' in variables
                else:
                    var_name = parameters.strip()
                    variables['last'] = var_name in variables
            else: warn(f'UNEXP LINE {current_line+1}')
            current_line += 1
    except Exception as e:
        warn(f'UNEXP ERR IN LINE {current_line+1}')
        if debug_mode: warn(f'The exception raised was:\n\n\n{e}')
        if not disable_warnings: raise
    return variables

run(program)

if debug_mode: print('\n')

# By the way, nobody is looking at the source code, right?
