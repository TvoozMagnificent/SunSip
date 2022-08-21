# The SunSip official guide

## Installation

First, you have to install python via python.org. You might already have it installed, or you might not.

SunSip can be installed from source or via `pip`. To install SunSip, use:

```bash
pip install SunSip
```

Or whatever way you use `pip`.

## Execution

SunSip code can be named with any extension, although the preferred extension is either none, `.sunsip`, `.snsp`, or `.slwnsnbp`.

After writing the SunSip code, you can execute it using

```bash
python -m SunSip program [options]
```

Or whatever way you use `python`. Include the `-m` flag, and substitute `program` for the path to your program, including the file name and extension.

For a list of options, refer to the help menu accessible via `python -m SunSip --help`.



**Note: when using the `--help` flag, the usage says `python3 main.py program.slwnsnbp [options]`, which is inaccurate.**
