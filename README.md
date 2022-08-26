# The SunSip official guide

## Table of Contents

- [Introduction](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#introduction)
- [Installation](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#installation)
- [Execution (Installation via `pip`)](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#execution-installation-via-pip)
- [Execution (Installation from source)](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#execution-installation-from-source)
- [Test Your Installation](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#test-your-installation)
- [Debugging](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#debugging)
- [Suppressing Warnings](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#suppressing-warnings)
- [Contributing](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#contributing)
- [I found a bug!!!](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#i-found-a-bug)
- [Learn SunSip: Refer to the Wiki](https://github.com/TvoozMagnificent/SunSip/wiki)
- [Research](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#research)
- [Trailer](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#trailer)
- [About Me](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#about-me)

## Introduction

SunSip, SLWNSNBP, or Simple Language Which Name Shall Not Be Pronounced, is a Turing Complete, Practical, Whitespace Insignificant,
Simple programming language (which name shall not be pronouced). SunSip is based on variables, with a simple concept and syntax,
designed to be beginner friendly. There are goals to turn it into a golfing language (by shortening instructions, et cetera.,) but that
is currently just a thought. The slogan is, `800 lines of code, for a good coding experience`. This is a project that I am working on
in order to apply for a certain science club. You can refer to the [Research](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#research)
section for details.

## Installation

First, you have to install python via python.org. You might already have it installed, or you might not.<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186843644-771e32f4-bc7b-4856-8a69-893b957905a2.png">


SunSip can be installed from source or via `pip`. To install SunSip via `pip`, use:

```bash
pip install SunSip
```

Or whatever way you use `pip`.

Currently, the `pip` version might be outdated.

## Execution (Installation via `pip`)
<img width="961" alt="image" src="https://user-images.githubusercontent.com/98521363/186843632-03ac9a9c-c728-4aff-878b-4e6bd897a7f7.png">

SunSip code can be named with any extension, although the preferred extension is either none, `.txt`, `.sunsip`, `.snsp`, or `.slwnsnbp`.

After writing the SunSip code, you can execute it using

```bash
python -m SunSip program [options]
```

Or whatever way you use `python`. Include the `-m` flag, and substitute `program` for the path to your program, including the file name and extension.

For a list of options, refer to the help menu accessible via `python -m SunSip --help`.

```
    Syntax: python -m SunSip program [options]
    Options:
        --help : Print this help message and exit.
        -d     : Debug mode.
        -v     : Verbose mode.
        -w     : Disable warnings.
```

**Note: When using the `--help` flag, the usage says `python3 main.py program.slwnsnbp [options]`, which is inaccurate.**

**Note: The terminal would warn, `<snip>: No module named SunSip.__main__; 'SunSip' is a package and cannot be directly executed`. Ignore such warnings.**

## Execution (Installation from source)

SunSip code can be named with any extension, although the preferred extension is either none, `.txt`, `.sunsip`, `.snsp`, or `.slwnsnbp`.

After writing the SunSip code, you can execute it using

```bash
python pathtoinit pathtoprogram [options]
```

Or whatever way you use `python`. Substitute `program` for the path to your program, including the file name and extension, and `pathtoinit` is the path to the `__init__.py` file.

For a list of options, refer to the help menu accessible via `python pathtoinit --help`, where `pathtoinit` is the path to the `__init__.py` file.

```
    Syntax: python pathtoinit pathtoprogram [options]
    Options:
        --help : Print this help message and exit.
        -d     : Debug mode.
        -v     : Verbose mode.
        -w     : Disable warnings.
```

**Note: When using the `--help` flag, the usage says `python3 main.py program.slwnsnbp [options]`, which is inaccurate.**

## Test Your Installation

If you haven't installed SunSip, do so by referring to the [Installation Section](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#installation).

First, create a folder on your desktop called `hellosnsp`. This folder will store all of your programs.
Create a text file named `firstprogram.txt` inside the folder, and write:

```
comment this should print hello world
set to "Hello, World! "
out
```

Execute the file (see the [Execution Sections](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#table-of-contents)).
It should produce the output:

```
Hello, World! 
```

## Debugging

If you need to debug your code, use the `-d` flag. This will output the parsed program first:

```
Program:
[['#', 'math support'], ['', ''], ['set', '180 to 180'], ['set', '5 to 5'], ['set', '4 to 4'], ['set', '1 to 1'], ['set', 'number to 1'], ['set', 'to "'], ['out', ''], ['set', 'empty to " "'], ['', ''], ['set', 'to "'], ['calc', 'type number'], ['calc', 'type last number'], ['set', 'length to'], ['calc', 'subtraction 5 length'], ['set', 'i to'], ['set', 'stack to []'], ['calc', 'push stack number'], ['set', 'stack to last'], ['', ''], ['calc', 'push stack empty'], ['set', 'stack to last'], ['calc', 'subtraction i 1'], ['set', 'i to'], ['calc', 'less i 1'], ['calc', 'multiplication last 4'], ['skip', ''], ['', ''], ['set', 'to 10'], ['back', ''], ['', ''], ['calc', 'factorial number'], ['calc', 'push stack last'], ['set', 'stack to'], ['set', 'to "'], ['calc', 'join stack'], ['out', ''], ['calc', 'addition number 1'], ['set', 'number to'], ['set', 'to 40'], ['calc', 'greater number last'], ['calc', 'multiplication last 4'], ['skip', ''], ['', ''], ['set', 'to 36'], ['back', ''], ['', ''], ['set', 'to "'], ['out', '']]
```

and after each line will print the current line, current instruction, current parameters, and current variable values.

```
Current Line: 49

Instruction: out

Parameters: 

Variables: {'180': 180, 'last': '', '5': 5, '4': 4, '1': 1, 'number': 41, 'empty': ' ', 'length': 2, 'i': 0, 'stack': [40, ' ', ' ', ' ', 815915283247897734345611269596115894272000000000]}
```

## Suppressing warnings

Take the example program,

```
# math support

set 180 to 180
set 5 to 5
set 4 to 4
set 1 to 1
set number to 1
set to "
out
set empty to " "

set to "
calc type number
calc type last number
set length to
calc subtraction 5 length
set i to
set stack to []
calc push stack number
set stack to last

calc push stack empty
set stack to last
calc subtraction i 1
set i to
calc less i 1
calc multiplication last 4
skip

set to 10
back

calc factorial number
calc push stack last
set stack to
set to "
calc join stack
out
calc addition number 1
set number to
set to 40
calc greater number last
calc multiplication last 4
skip

set to 36
back

set to "
out
```

When you execute it, it will cause warnings, and output the following:

```
WARNING: UNEXP LINE 1



WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

1    1

WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

2    2

WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

3    6

WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

4    24

WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

5    120

WARNING: IMPL TYPE CONV AT LINE 37


WARNING: IMPL TYPE CONV AT LINE 37

<snip>
```

(with warnings in red.) Warnings are parts where your program could've gone wrong. To suppress them, for cleaner output, use the `-w` flag:

```
1    1
2    2
3    6
4    24
5    120
6    720
7    5040
8    40320
9    362880
10   3628800
11   39916800
12   479001600
13   6227020800
14   87178291200
15   1307674368000
16   20922789888000
17   355687428096000
18   6402373705728000
19   121645100408832000
20   2432902008176640000
21   51090942171709440000
22   1124000727777607680000
23   25852016738884976640000
24   620448401733239439360000
25   15511210043330985984000000
26   403291461126605635584000000
27   10888869450418352160768000000
28   304888344611713860501504000000
29   8841761993739701954543616000000
30   265252859812191058636308480000000
31   8222838654177922817725562880000000
32   263130836933693530167218012160000000
33   8683317618811886495518194401280000000
34   295232799039604140847618609643520000000
35   10333147966386144929666651337523200000000
36   371993326789901217467999448150835200000000
37   13763753091226345046315979581580902400000000
38   523022617466601111760007224100074291200000000
39   20397882081197443358640281739902897356800000000
40   815915283247897734345611269596115894272000000000
```

It is not recommended to turn off warnings while debugging, but it is allowed to use `-d -w` or `-w -d`.

**Note: `-dw` or `-wd` is not supported by SunSip.**

# Contributing

I want to contribute! How?

Method 1, create a pull request. Method 2, edit directly. Method 3, open an issue.

We accept contributions that add functionality, fixxes bugs, or raises bugs. **However, code editors must create a pull request
or open an issue, and the issue must be passed before they do the editting.**

**If your code implies a bug, please explicitly paste the output, warnings, and debuggings.**

# I found a bug!!!

See [Contributing](https://github.com/TvoozMagnificent/SunSip/blob/main/README.md#contributing).

# Research

As I have said, this is a research project.

---

<img width="720" alt="image" src="https://user-images.githubusercontent.com/98521363/186842342-01dc0a56-1f35-450d-8503-b5142c44affd.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842476-6fb5a480-87e4-4bd9-ba1a-ff024a8c5747.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842509-2ebd5534-0888-4739-b979-b9fa7cf72263.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842722-d0ff2259-ddb3-4e01-88df-9cbc75d1f26b.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842769-7e719b66-ea41-4f18-bd4f-a4473f207b60.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842795-be059edb-68d2-4143-a047-ac4a74a564b7.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186842824-cff52f36-675d-4db0-8bf8-9d9eb761cb75.png">

---

# Trailer

---

<img width="961" alt="image" src="https://user-images.githubusercontent.com/98521363/186843509-6806689b-516a-47db-be87-32dcb03e348f.png">

---

# About Me

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186843928-cff2cf78-d72b-4ab4-be76-856bfd514502.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186843830-e9315aae-92a0-4c79-a49b-688ad7ec62f6.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186843975-a5430c6f-f3fd-45cd-ae87-9f8803a44264.png">

---

<img width="828" alt="image" src="https://user-images.githubusercontent.com/98521363/186844021-64996a74-8c0a-4730-bc2b-a3afe7df0085.png">

---

