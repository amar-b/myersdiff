# myersdiff
Python implementation of Myers diff algoirthm. Follows implementation described in (James Coglan's blog)[https://blog.jcoglan.com]. Displays ANSI colors in applicable terminals.

### Example usage
```
$ python myersdiff.py "abcef" "abXefg"
  a
  b
- c
+ X
  e
  f
+ g
```

### Help
```
usage: myersdiff.py [-h] [-t {file,str}] left right

Myers Differ

positional arguments:
  left           left file path or string
  right          right file path or string

optional arguments:
  -h, --help     show this help message and exit
  -t {file,str}  input type: file or string (default: str)
```
