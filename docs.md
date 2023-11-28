# Funlang language docs.
This documentation let you learn on how to make scripts for\
Funlang and many other.
## Table of contents
- [Intro](#intro)
- [Getting started](#getting-started)
- [Headers](#headers)
- [Functions](#functions)
  - [SAY](#say)
  - [MEET](#meet)
  - [SET](#set)
  - [PLS](#pls)
  - [THINK](#think)
  - [SYSTEM](#system)
  - [BYE](#bye)
  - [LOOP](#loop)
  - [WHEN](#when)
  - [ASK](#ask)
  - [RANDOM](#random)
  - [ERROR](#error)
- [Conclusion](#conclusion)
## Intro
Funlang is a programming language designed for simplicity **(maybe not lol)** and ease of use. It provides a set of functions that allow you to perform various operations, such as printing messages, manipulating variables, executing system commands, and more.
## Getting started
To get started with Funlang, you need to have the Funlang interpreter installed on your system. You can download the interpreter from this GitHub repository. 

Once you have the Funlang interpreter installed, you can create a new Funlang script file with a `.fun` or `.funlang` extension. In this file, you can write your Funlang code using the available functions and syntax.
## Headers
<sup>The headers was removed, cause its time wasting to write whole name, description, author in your code.</sup>
## Functions
### SAY
Say function let you display text you specified. But first, you need to use [PLS](#pls) STDIO to use it.
### MEET
Creates an new variable.
### SET
Sets an variable contents to contents you specified.
### PLS
Gives you permission to what you want.\
Possible permissions are
- `STDIO`: Allows the use of standard i/o functions.
- `TIME`: Allows the use of time-related functions, such as `THINK`.
- `OS`: Allows the use of system-related functions, such as `SYSTEM`.
- `RANDOM`: Allows the use of random number generation functions, such as `RANDOM`.
### THINK
Halts for N ms. But first you need to have permission for time.
### SYSTEM
Runs system command.
### BYE
Exits program with specified error code.
### LOOP
Creates an loop.\
Must add `LOOPEND` at end of functions you want to be in loop to prevent an error.
### WHEN
Same as loop, but executes once and
must add `WHENEND` at end of functions you want to be in when to prevent an error.
### ASK
Asks user for input.\
The arguments for function is `Where-to-store Question`.
### RANDOM
Picks an random number.\
Arguments are `VAR MIN MAX`.
### ERROR
Throws an error with reason you specified.
## Conclusion
This documentation provided an overview of the functions and features available in the Funlang programming language. You learned about the various functions, such as `PLS`, `SAY`, `MEET`, `SET`, `THINK`, `SYSTEM`, `BYE`, `LOOP`, `WHEN`, `ASK`, and `RANDOM`, and how to use them in your Funlang scripts.

With this knowledge, you can start creating your own Funlang scripts and explore the possibilities of this simple programming language.

Happy coding!
