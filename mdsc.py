import mdsc

__version__ = "0.1"

c = mdsc.Compiler()
code = c.compile("code.mdsc")
with open('output.mdscx', 'w') as f:
    f.write(code)
