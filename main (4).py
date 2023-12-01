#!/usr/bin/env python
import argparse
import os
import random
import re
import sys
import time


def get(file):
  with open(file) as f:
    data = f.read()
  return data

def parse(line):
  split = line.split()
  if len(split) != 0:
    return split
def parsestr(string, env):
  for i in env:
    string = string.replace(f'<{i}>', str(env[i]))
  string = re.sub(r"<NEWLINE>", "\n", string)
  string = re.sub(r"<.*>", "<UNKNOWN?>", string)
  return string

def error(reason,line,scr):
  reason = reason.upper()
  print('OH NO!')
  print('THERES AN ERROR IN YA SCRIPT.')
  print('TEH ERROR REASON IS:')
  print(reason)
  print('AND IT HAPPEND AT LINE',line+1)
  print(scr)
  quit()
def findloopstop(lines,c):
  for e,i in enumerate(lines[c::]):
    if i == 'LOOPEND':
      return e
  error('no loop end?',c,"")
def findifend(lines,c):
  for e,i in enumerate(lines[c::]):
    if i == 'WHENEND':
      return e
  error('no when end?',c,"")
def findfuncend(lines,c):
  for e,i in enumerate(lines[c::]):
    if i == 'ENDFUNCTION':
      return e
  error('no function end?',c,"")
def runline(line,canuseos,canusestdio,canusewait,canuserandom,env,c,code,safe,args,functions):
  parsed = parse(line)
  if not parsed:
    return
  if parsed[0] == 'SAY':
    if canusestdio:
      print(parsestr(' '.join(parsed[1:]), env))
    else:
      error('please, ask stdio for permission to say anything before saying',c,line)
  elif parsed[0] == 'MEET':
    if parsed[1] not in env:
      env[parsed[1]] = None
    else:
      error('variable already exists',c,line)
  elif parsed[0] == 'SET':
    if parsed[1] in env:
      env[parsed[1]] = eval(parsestr(' '.join(parsed[2:]),env), {'__builtins__': None})
    else:
      error('variable does not exist',c,line)
  elif parsed[0] == 'PLS':
    if parsed[1] == 'STDIO':
      canusestdio = True
    elif parsed[1] == 'TIME':
      canusewait = True
    elif parsed[1] == 'OS':
      canuseos = True
    elif parsed[1] == 'RANDOM':
      canuserandom = True
    else:
      error('i dont understand, what do you need?',c,line)
  elif parsed[0] == "THINK":
    if canusewait:
      time.sleep(int(parsed[1])/1000)
    else:
      error('you dont have time',c,line)
  elif parsed[0] == "RANDOM":
    if canuserandom:
      try:
        env[parsed[1]] = random.randint(int(parsestr(parsed[2],env)),
                                        int(parsestr(parsed[3],env)))
      except TypeError:
        error('using randomize on a non-number',c,line)
    else:
      error('no randomness?',c,line)
  elif parsed[0] == 'SYSTEM':
    if canuseos:
      if not safe:
        os.system(parsestr(' '.join(parsed[1:]), env))
      else:
        print('Detected an system call:',parsestr(' '.join(parsed[1:]), env))
    else:
      error('any permission to use system?',c,line)
  elif parsed[0] == 'BYE':
    sys.exit(int(parsed[1]))
  elif parsed[0] == 'LOOP':
    run = True
    loopstart = c + 1
    loopend = findloopstop(code,c) + c
    while run:
      run = eval(parsestr(' '.join(parsed[1:]),env), {'__builtins__': None})
      emulate2(code[loopstart+1:loopend], canuseos,canusestdio,canusewait,canuserandom,env,safe,args,functions)
    return ("SKIP",loopend-loopstart)
  elif parsed[0] == 'WHEN':
    loopstart = c + 1
    loopend = findifend(code,c) + c
    if eval(parsestr(' '.join(parsed[1:]),env), {'__builtins__': None}):
      emulate2(code[loopstart+1:loopend], canuseos,canusestdio,canusewait,canuserandom,env,safe,args,functions)
    return ("SKIP",loopend-loopstart)
  elif parsed[0] == 'FUNCTION':
    loopstart = c + 1
    loopend = findfuncend(code,c) + c
    functions[parsed[1]] = code[loopstart+1:loopend]
    return ("SKIP",loopend-loopstart)
  elif parsed[0] in functions:
    emulate2(functions[parsed[0]], canuseos,canusestdio,canusewait,canuserandom,env,safe,parsed[1:],functions)
  elif parsed[0] == 'ASK':
    if canusestdio:
      env[parsed[1]] = input(parsestr(' '.join(parsed[2:]), env))
    else:
      error('please, ask stdio for permission to ask anything before asking',c,line)
  elif parsed[0] == 'ERROR':
    error(parsestr(' '.join(parsed[1:]), env),c,line)
  elif parsed[0] == "GET":
    if parsed[2] in env:
      try:
        env[parsed[1]] = env[parsed[2]][int(parsed[3])]
      except ValueError:
        env[parsed[1]] = env[parsed[2]][parsed[3]]
      except TypeError:
        error('using get on non-list',c,line)
      except IndexError:
        error('index out of range',c,line)
    else:
      error('variable does not exist',c,line)
  elif parsed[0] == "ARG":
    try:
      env[parsed[1]] = args[int(parsed[3])]
    except IndexError:
      error('index out of range',c,line)
  else:
    error('function doesnt exist',c,line)
  return (canuseos,canusestdio,canusestdio,canuserandom,env,args, functions)

def emulate(code,safe=False):
  env = {}
  canusestdio = False
  canusewait = False
  canuseos = False
  canuserandom = False
  args = []
  functions = {}
  code = code.split('\n')
  skiplines = 0
  for c,line in enumerate(code[1:]): # slice one line cause headers was removed😢
    if skiplines < 1:
      ret = runline(line, canuseos,canusestdio,canusewait,canuserandom,env,c,code,safe,args,functions)
      if ret:
        if ret[0] == 'SKIP':
          skiplines += ret[1]
        else:
          canuseos, canusewait, canusestdio, canuserandom, env, args,functions = ret
    else:
      skiplines -= 1
def getname(data):
  y = data.split('\n')
  line = y[1]
  parsed = parse(line)
  return ' '.join(parsed[2:])
def getauthor(data):
  y = data.split('\n')
  line = y[2]
  parsed = parse(line)
  return ' '.join(parsed[2:])
def getdesc(data):
  y = data.split('\n')
  line = y[3]
  parsed = parse(line)
  return ' '.join(parsed[1:])
  
def emulate2(code,canuseos,canusestdio,canusewait,canuserandom,env,safe,args,functions):
  for c,line in enumerate(code):
    runline(line,canuseos,canusestdio,canusewait,canuserandom,env,c,code,safe,args,functions)

parser = argparse.ArgumentParser(description='Funlang intepreter',prog="funlang",
                  epilog="funlang (c) 2023 - 2023 - github.com/simpleuserdontwatch",
                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('file', type=str, help='file to process')
parser.add_argument('--safe', help='Run code safetly (disables system function)', 
                    action='store_true')
args = parser.parse_args()
file = args.file
try:
  data = get(file)
  if not args.safe:
    emulate(data)
  else:
    emulate(data, True)
except FileNotFoundError:
  print('File not found!')