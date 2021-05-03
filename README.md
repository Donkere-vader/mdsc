# Mindustry Compiler | MDSC

A compiler to write better and easier code for the [mindustry game](https://github.com/Anuken/Mindustry) logic.

## Disclaimer

This project is far from finished and doesn't contain nearly all the functionality of the built in logic system. This is just a MVP.

## The language

The language got inpsiration from mainly python and rust. It should be very straight forward.

## Programming in MDSC

If you have programmed before it shouldn't be hard to understand.

### Comments

Comments start with a ``//``. Everything from the comment to the end of the line will be ignored.

### In game objects

Getting an in game object is done with ``%DEFINE``. (This is basically the same as just setting a variable, but this way it is clear that it is about a game object).

To reference message1 (as in game object) from the code as msg_block you would write:

```mdsc
%DEFINE msg_block = message1;
```

### Variables

Variables are set in a very straight forward way.

Either use:

```mdsc
let varname = "varvalue";
```

or

```mdsc
var varname = "varvalue";
```

or

```mdsc
varname = "varvalue";
```

If you use ``var``, ``let`` or none doesn't matter for the code.

### Writing functions

defining a function is very rust-like. To define a function named 'hello_world' you would write:

```mdsc
fn hello_world() {
    // fn body
}
```

### Flags

You can add a flag to a function.  
A flag is defined like so:

```mdsc
#[FLAG_NAME]
```

All flags will be explained below.

#### MACHINE

the ``#[MACHINE]`` flag. This flag makes a function or code block behave like "native" mindusty logic code. This is however a slightly different code.

There are two differences with native mindustry code when writing machine code in MDSC.

1. All lines in machine mdsc should end with a semi-colon ``;``.
2. To reference variables from mdsc you need to wrap them in arrows like so: ``<varname>`` this has to do with how variables are handeled. The compiler renames variables to prevent context conflicts.

### Roadmap

I'm planning to add some more feautures. Listed below:

- [ ] Import
- [ ] Support all mindustry logic blocks  
  This will be done by creating a std library
  - [ ] Read
  - [ ] Write
  - [ ] Draw
  - [ ] Print
  - [ ] Draw Flush
  - [ ] Print Flush
  - [ ] Get Link
  - [ ] Control
  - [ ] Rader
  - [ ] Sensor
  - [ ] Set
  - [ ] Operation
  - [ ] End
  - [ ] Jump
  - [ ] Unit Bind
  - [ ] Unit Control
  - [ ] Unit Radar
  - [ ] Unit Locate
- [ ] Logic (if statements)
- [ ] Loops
  - [ ] While
  - [ ] For
- [ ] Different data types
  - [ ] list
  - [ ] hash table / dict
