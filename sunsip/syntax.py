import sys
import rich
import argparse


# Simple Syntax Highlighter for SunSip

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
    parser = argparse.ArgumentParser(dscription="SunSip syntax highlighter")
    parser.add_argument("program", help="The path to the program to highlight")

    args = parser.parse_args()
    try:
        with open(args.program, "r") as f:
            program = f.read()
    except FileNotFoundError:
        print(f'\033[91mSorry, I can not find the file: '
          f'{args.program}.'
          f'\nCheck the path, name, and file extension.'
          f'\nFor usage help, use the --help option.\033[0m\n')
        sys.exit(1)

    rich.print(syntax_highlight(program))

if __name__ == "__main__":
    main()