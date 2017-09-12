#!/usr/bin/python3

# funge.py -- a Funge interpreter written in Python
#
# usage: funge.py <prog.fu>

dim = (80,80)

import sys
import logging
logging.addLevelName( logging.WARNING, "\033[1;31m%-8s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%-8s\033[1;0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName( logging.CRITICAL, "\033[1;41m%-8s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

logging.basicConfig(format='%(levelname)-8s | %(message)s',
                    level=logging.INFO)

from datetime import datetime
import random

class Prog:
  def __init__(self, src):
      self.cursor = [0,0]
      self.delta = (1,0)

      src_lines = src.split('\n')
      n_lines = len(src_lines)
      longest_line = max(map(len,src_lines))

      self.src = '\n'.join(f'{s:<{longest_line}}' for s in src_lines)
      self.dim = longest_line, n_lines

      logging.debug(f'The source {self.dim}:\n'+self.src)

  def _coords(self, x, y):
    return x + (self.dim[0]+1) * y

  def get(self, pos = None):
    logging.debug(f'{self.dim}, {self.cursor}, {self.delta}, {pos}')
    
    x,y = self.cursor if pos is None else pos
    logging.debug(f'{self._coords(x,y)}')

    assert x >= 0 and x < self.dim[0]
    assert y >= 0 and y < self.dim[1]
    
    return self.src[self._coords(x,y)]

  def put(self, pos, val):
    off = self._coords(*pos)
    logging.debug(f'source :\n'+self.src)
    self.src = self.src[:off] + chr(val) + self.src[off+1:]
    logging.debug(f'p {pos}, {val}, {off}')
    logging.debug(f'The source {self.dim}:\n'+self.src)

  def advance(self):
    self.cursor = ( (self.cursor[0] + self.delta[0]) % self.dim[0],
                    (self.cursor[1] + self.delta[1]) % self.dim[1] )
    

class Stack(list):
  def pop(self, *args):
    return super().pop(*args) if len(self) > 0 else 0

  def push(self, val):
    self.append(val)

  def __getitem__(self, key):
    return super().__getitem__(key) if len(self) > 0 else 0
  
if __name__ == '__main__':
  logging.info('Let the funge begin!')
  if len(sys.argv) != 2:
    logging.fatal(f'Usage: {sys.argv[0]} <prog.fu>')
    sys.exit(1)

  # read funge program
  prog_name = sys.argv[1]

  # prog will hold the funge program source
  with open(prog_name) as f: prog = Prog(f.read())
  if not prog: sys.exit(2)

  # initialise stack and cursor
  stack = Stack()

  logging.info(' ––– funge starting –––')

  string_mode = False
  reached_end = False
  while not reached_end:
    cmd = prog.get()
    logging.debug(f'{cmd} at {prog.cursor}')
    
    if cmd == '"': string_mode = not string_mode
    elif string_mode: stack.push(ord(cmd))
    elif cmd in '1234567890': stack.push(int(cmd))
    elif cmd == ' ': pass

    # program counter direction
    elif cmd == '>': prog.delta = (1,0)
    elif cmd == '<': prog.delta = (-1,0)
    elif cmd == '^': prog.delta = (0,-1)
    elif cmd == 'v': prog.delta = (0,1)
    elif cmd == '?': prog.delta = random.choice(((0,1),(1,0),(-1,0),(0,-1)))
    elif cmd == '#': prog.advance()

    # arithmetics
    elif cmd == '+': stack.push(stack.pop() + stack.pop())
    elif cmd == '-': stack.push(stack.pop(-2) - stack.pop())   
    elif cmd == '*': stack.push(stack.pop() * stack.pop())
    elif cmd == '/': stack.push(int(stack.pop(-2) // stack.pop()))
    elif cmd == '%': stack.push(stack.pop(-2) % stack.pop())
    elif cmd == '!': stack.push(int(not bool(stack.pop())))
    elif cmd == '`': stack.push(int(stack.pop(-2) > stack.pop()))

    # conditionals
    elif cmd == '_': prog.delta = (-1,0) if stack.pop() else (1,0)
    elif cmd == '|': prog.delta = (0,-1) if stack.pop() else (0,1)

    # stack manipulation
    elif cmd == ':': stack.push(stack[-1])
    elif cmd == '\\': a,b = stack.pop(), stack.pop(); stack.push(a); stack.push(b)
    elif cmd == '$': stack.pop()

    # io
    elif cmd == '.': sys.stdout.write(str(stack.pop())); sys.stdout.flush()
    elif cmd == ',': sys.stdout.write(chr(stack.pop())); sys.stdout.flush()
    elif cmd == '&': stack.push(int(input()))
    elif cmd == '~': stack.push(ord(input()[0]))

    # self modification
    elif cmd == 'g': y,x = stack.pop(), stack.pop(); stack.push(ord(prog.get((x, y))))
    elif cmd == 'p': y,x,v = stack.pop(), stack.pop(), stack.pop(); prog.put((x, y), v)

    # end
    elif cmd == '@': reached_end = True

    else: logging.error(f'command \'{cmd}\' ({ord(cmd)}) at {prog.cursor} not implemented yet')

    if cmd not in '<>v^ ': logging.debug(f'{stack}')

    #~ logging.debug(reached_end)
    
    # move cursor
    if not reached_end: prog.advance()

  #~ sys.stdout.flush()
  logging.info(' ––– funge ended –––')
