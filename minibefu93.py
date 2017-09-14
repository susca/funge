#!/usr/bin/python3
# minibefu93.py -- a minimal Befunge93 interpreter written in Python
# usage: minibefu93.py <prog.fu>

import sys,random
class Prog:
  def __init__(self, src):
      self.cursor = [0,0]
      self.delta = (1,0)
      self.dim = 80,25
      
      src_lines = src.split('\n')
      [src_lines.append('') for _ in range(len(src_lines),self.dim[1])]
      self.src = '\n'.join(f'{s:<{self.dim[0]}}' for s in src_lines)

  def _coords(self, x, y):
    return x + (self.dim[0]+1) * y

  def get(self, pos = None):
    
    x,y = self.cursor if pos is None else pos

    return self.src[self._coords(x,y)]

  def put(self, pos, val):
    off = self._coords(*pos)
    self.src = self.src[:off] + chr(val) + self.src[off+1:]

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
  # prog will hold the funge program source
  with open(sys.argv[1]) as f: prog = Prog(f.read())

  # initialise stack and cursor
  stack = Stack()

  string_mode = False
  while True:
    cmd = prog.get()
    
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
    elif cmd == '@': break
    
    # move cursor
    prog.advance()
