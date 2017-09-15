#!/usr/bin/python3

# funge.py -- a Funge interpreter written in Python
#
# usage: funge.py <prog.fu>

import sys
import logging as logg
logg.addLevelName(logg.WARNING, "\033[1;31m%-8s\033[1;0m" %
                  logg.getLevelName(logg.WARNING))
logg.addLevelName(logg.ERROR, "\033[1;41m%-8s\033[1;0m" %
                  logg.getLevelName(logg.ERROR))
logg.addLevelName(logg.CRITICAL, "\033[1;41m%-8s\033[1;0m" %
                  logg.getLevelName(logg.CRITICAL))

logg.basicConfig(format='%(levelname)-8s | %(message)s', level=logg.INFO)

import random

class Prog:
  def __init__(self, src):
    self.cursor = (0, 0)
    self.delta = (1, 0)
    self.dim = (80, 25)

    src_lines = src.split('\n')
    [src_lines.append('') for _ in range(len(src_lines), self.dim[1])]
    self.src = '\n'.join(f'{s:<{self.dim[0]}}' for s in src_lines)

    assert all(x == self.dim[0] for x in map(len, self.src.split('\n')))
    assert self.src.count('\n') == self.dim[1]-1

    logg.debug(f'The source {self.dim}:\n'+self.src)

  def _coords(self, x, y):
    return x + (self.dim[0]+1) * y

  def get(self, pos=None):
    logg.debug(f'{self.dim}, {self.cursor}, {self.delta}, {pos}')

    x, y = self.cursor if pos is None else pos
    logg.debug(f'{self._coords(x,y)}')

    assert x >= 0 and x < self.dim[0]
    assert y >= 0 and y < self.dim[1]

    return self.src[self._coords(x, y)]

  def put(self, pos, val):
    off = self._coords(*pos)
    logg.debug(f'source :\n'+self.src)
    self.src = self.src[:off] + chr(val) + self.src[off+1:]
    logg.debug(f'p {pos}, {val}, {off}')
    logg.debug(f'The source {self.dim}:\n'+self.src)

  def advance(self):
    self.cursor = ((self.cursor[0] + self.delta[0]) % self.dim[0],
                   (self.cursor[1] + self.delta[1]) % self.dim[1])


class Stack(list):
  def pop(self, *args):
    return super().pop(*args) if self else 0

  def push(self, val):
    self.append(val)

  def __getitem__(self, key):
    return super().__getitem__(key) if self else 0

if __name__ == '__main__':
  logg.info('Let the funge begin!')
  if len(sys.argv) != 2:
    logg.fatal(f'Usage: {sys.argv[0]} <prog.fu>')
    sys.exit(1)

  # read funge program
  prog_name = sys.argv[1]

  # prog will hold the funge program source
  with open(prog_name) as f: prog = Prog(f.read())
  if not prog: sys.exit(2)

  # initialise stack and cursor
  stack = Stack()

  logg.info(' ––– funge starting –––')

  string_mode = False
  reached_end = False
  while not reached_end:
    cmd = prog.get()
    logg.debug(f'{cmd} at {prog.cursor}')

    if cmd == '"': string_mode = not string_mode
    elif string_mode: stack.push(ord(cmd))
    elif cmd in '1234567890': stack.push(int(cmd))
    elif cmd == ' ': pass

    # program counter direction
    elif cmd == '>': prog.delta = (1, 0)
    elif cmd == '<': prog.delta = (-1, 0)
    elif cmd == '^': prog.delta = (0, -1)
    elif cmd == 'v': prog.delta = (0, 1)
    elif cmd == '?': prog.delta = random.choice(((0, 1), (1, 0), (-1, 0), (0, -1)))
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
    elif cmd == '_': prog.delta = (-1, 0) if stack.pop() else (1, 0)
    elif cmd == '|': prog.delta = (0, -1) if stack.pop() else (0, 1)

    # stack manipulation
    elif cmd == ':': stack.push(stack[-1])
    elif cmd == '\\': a, b = stack.pop(), stack.pop(); stack.push(a); stack.push(b)
    elif cmd == '$': stack.pop()

    # io
    elif cmd == '.': sys.stdout.write(str(stack.pop())); sys.stdout.flush()
    elif cmd == ',': sys.stdout.write(chr(stack.pop())); sys.stdout.flush()
    elif cmd == '&': stack.push(int(input()))
    elif cmd == '~': stack.push(ord(input()[0]))

    # self modification
    elif cmd == 'g': y, x = stack.pop(), stack.pop(); stack.push(ord(prog.get((x, y))))
    elif cmd == 'p': y, x, v = stack.pop(), stack.pop(), stack.pop(); prog.put((x, y), v)

    # end
    elif cmd == '@': reached_end = True

    else: logg.error(f'command \'{cmd}\' ({ord(cmd)}) at {prog.cursor} not implemented yet')

    if cmd not in '<>v^ ': logg.debug(f'{stack}')

    #~ logg.debug(reached_end)

    # move cursor
    if not reached_end: prog.advance()

  #~ sys.stdout.flush()
  logg.info(' ––– funge ended –––')
