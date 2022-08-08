First, to get the hang of SLWNSNBP (Sun Sip), lets... 

# Analyze a sample program:

```Sunsip
comment truth machine
comment set input string
set to "
comment get input
in
comment output
out
comment make integer
calc int
comment default to integer and skip that many lines
skip
exit # exit program if 0
comment repeatedly out if 1
out
back
```

## Line 1: `comment truth machine`

Well, this is a comment. Pretty obvious.

A truth machine is a program that takes an integer 0 or 1.
If the integer is 0, the program prints 0 and exits.
If the integer is 1, the program prints 1 infinitely.

## Line 2: `comment set input string`

Another comment.

## Line 3: `set to "`

`set` takes two parameters, seperated by `to`. 
The first parameter is the name of the variable.
The second parameter is the value of the variable.
In this case, the variable name is omitted.
The variable name defaults to `last`.
The variable value is an empty string.
Thus, we are setting `last` to an empty string.

## Line 4: `comment get input`

Another comment.

## Line 5: `in`

`in` takes one parameter, a variable name,
and reads the value. It then asks for user input
and sets `last` to the input. Here, the
variable name defaults to `last`, and thus
the program prompts the user with an empty string.
The input can either be `0` or `1`, as a string.

## Line 6: `comment output`

Another comment.

## Line 7: `out`

`out` takes one parameter, a variable name,
and prints the value. Here, the variable name
defaults to `last`, and thus the program prints
the user input.

## Line 8: `comment make integer`

Another comment.

## Line 9: `calc int`

`calc int` takes one parameter, a string,
and converts it to an integer. Thus, the string
is converted to `0` or `1`. If we used implied
conversion, we would have taken the length
of the string instead, which is not what we want.
We store the converted value to `last`.

## Line 10: `comment default to integer and skip that many lines`

Another comment.

## Line 11: `skip`

`skip` takes one parameter, an integer, and skips
that many lines. Here, the parameter defaults to
`last`, and thus skips that many lines.

If the input is `0`, the program exits via the next command,
`exit`. `exit` ignores all parameters.

## Line 12: `exit`

Explained above.

## Line 13: `comment repeatedly out if 1`

Another comment. This is only executed if the input is `1`.

## Line 14: `out`

Explained above. Outputs `1` (as that is the value in `last`).

## Line 15: `back`

Goes back `last` lines. In this case, it goes back to the
previous line, `out`, as `last` is `1` here.

# Documentation

Every line is a statement. Every statement's class is its first word. "Words" are splitted with spaces.

Whitespace is not important in Sun Sip. For instance, two newlines is the same as one. (However, it will impact the line number.)
Two spaces is the same as one. (Except in strings.) Lines strip by default.

The following are possible classes for statements:

## `comment`

Declares the line as a comment.

## `set [VAR=last] to [VAL=last]`

`last` is a special variable in Sun Sip: all variables default to `last` if unspecified.

`set variable to 123` sets the variable named `variable` to the integer value `123`.

`set to 123` sets the variable named `last` to `123`.

`set variable to` sets the variable named `variable` to whatever value `last` is.

`set to` sets the variable named `last` to whatever value `last` is. Not very helpful, but syntactically correct.

### There are many options for VAL:

- Integer, for instance 2786, -124897, 000000124, or -0
- Decimal, for instance 3.14, -0.0000, .14285714, or 3. (or even . if you want to, but why?)
- Sci.Int, for instance 3e98, 5123e38, -123456e9
- Sci.Dec, for instance .8E9, .999E.8, or even 1E-. (which equals 1.0E-0.0)
-    String, for instance "abc, "abcde", "ending with a quote"" (it is not possible to literally write a newline character)
- Character, for instance 'a, 'b, '', '", ' '
- \[\], empty list
- {}, empty set
- <>, empty stack
- Boolean, y for True, n for False
- And of course, `last`

## `in [VAR=last]`

Get user info for VAR and stores it into `last`. For instance,

```
set var to "How old are you?"
in var
```

Sets the variable `last` to the age of the user. `in` returns a string.

The same code can be shortened into:

```
set to "How old are you?
in
```

Which will instead use `last` for storing the string "How old are you?". Note that this way
the string will be overridden by user input.

















