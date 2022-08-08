First, to get the hang of SLWNSNBP, lets... 

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

# Line 1: `comment truth machine`

Well, this is a comment. Pretty obvious.

A truth machine is a program that takes an integer 0 or 1.
If the integer is 0, the program prints 0 and exits.
If the integer is 1, the program prints 1 infinitely.

# Line 2: `comment set input string`

Another comment.

# Line 3: `set to "`

`set` takes two parameters, seperated by `to`. 
The first parameter is the name of the variable.
The second parameter is the value of the variable.
In this case, the variable name is omitted.
The variable name defaults to `last`.
The variable value is an empty string.
Thus, we are setting `last` to an empty string.

# Line 4: `comment get input`

Another comment.

# Line 5: `in`

`in` takes one parameter, a variable name,
and reads the value. It then asks for user input
and sets `last` to the input. Here, the
variable name defaults to `last`, and thus
the program prompts the user with an empty string.
The input can either be `0` or `1`, as a string.

# Line 6: `comment output`

Another comment.

# Line 7: `out`

`out` takes one parameter, a variable name,
and prints the value. Here, the variable name
defaults to `last`, and thus the program prints
the user input.

# Line 8: `comment make integer`

Another comment.

# Line 9: `calc int`

`calc int` takes one parameter, a string,
and converts it to an integer. Thus, the string
is converted to `0` or `1`. If we used implied
conversion, we would have taken the length
of the string instead, which is not what we want.
We store the converted value to `last`.

# Line 10: `comment default to integer and skip that many lines`

Another comment.

# Line 11: `skip`

`skip` takes one parameter, an integer, and skips
that many lines. Here, the parameter defaults to
`last`, and thus skips that many lines.

If the input is `0`, the program exits via the next command,
`exit`. `exit` ignores all parameters.

# Line 12: `exit`

Explained above.

# Line 13: `comment repeatedly out if 1`

Another comment. This is only executed if the input is `1`.

# Line 14: `out`

Explained above. Outputs `1` (as that is the value in `last`).

# Line 15: `back`

Goes back `last` lines. In this case, it goes back to the
previous line, `out`, as `last` is `1` here.
