#!/usr/bin/python3
# minibefu93.py -- a minimal Befunge93 interpreter written in Python
# usage: minibefu93.py <prog.fu>
import sys,random
cursor=0,0
delta=1,0
dim=80,25
def coords(x,y):return x+dim[0]*y+y
def get(src,pos=None):
  x,y=cursor if pos is None else pos
  return src[coords(x,y)]
def put(src,pos,val):
  off=coords(*pos)
  return src[:off]+chr(val)+src[off+1:]
def advance():return (cursor[0]+delta[0])%dim[0],(cursor[1]+delta[1])%dim[1]
class Stack(list):
  def pop(self,*args):return super().pop(*args) if len(self)>0 else 0
  def push(self,val):self.append(val)
  def __getitem__(self,key):return super().__getitem__(key) if len(self)>0 else 0
with open(sys.argv[1]) as f:src=f.read()
lines=src.split('\n')
[lines.append('') for _ in range(len(lines),dim[1])]
src='\n'.join(f'{s:<{dim[0]}}' for s in lines)
stack=Stack()
s_mode=False
while True:
  cmd=get(src)
  if cmd=='"':s_mode=not s_mode
  elif s_mode:stack.push(ord(cmd))
  elif cmd in '1234567890':stack.push(int(cmd))
  elif cmd=='>':delta=(1,0)
  elif cmd=='<':delta=(-1,0)
  elif cmd=='^':delta=(0,-1)
  elif cmd=='v':delta=(0,1)
  elif cmd=='?':delta=random.choice(((0,1),(1,0),(-1,0),(0,-1)))
  elif cmd=='#':cursor=advance()
  elif cmd=='+':stack.push(stack.pop()+stack.pop())
  elif cmd=='-':stack.push(stack.pop(-2)-stack.pop())   
  elif cmd=='*':stack.push(stack.pop()*stack.pop())
  elif cmd=='/':stack.push(int(stack.pop(-2) // stack.pop()))
  elif cmd=='%':stack.push(stack.pop(-2) % stack.pop())
  elif cmd=='!':stack.push(int(not bool(stack.pop())))
  elif cmd=='`':stack.push(int(stack.pop(-2)>stack.pop()))
  elif cmd=='_':delta=(-1,0) if stack.pop() else (1,0)
  elif cmd=='|':delta=(0,-1) if stack.pop() else (0,1)
  elif cmd==':':stack.push(stack[-1])
  elif cmd=='\\':a,b=stack.pop(),stack.pop();stack.push(a);stack.push(b)
  elif cmd=='$':stack.pop()
  elif cmd=='.':sys.stdout.write(str(stack.pop()));sys.stdout.flush()
  elif cmd==',':sys.stdout.write(chr(stack.pop()));sys.stdout.flush()
  elif cmd=='&':stack.push(int(input()))
  elif cmd=='~':stack.push(ord(input()[0]))
  elif cmd=='g':y,x=stack.pop(),stack.pop();stack.push(ord(get(src,(x,y))))
  elif cmd=='p':y,x,v=stack.pop(),stack.pop(),stack.pop();src=put(src,(x,y),v)
  elif cmd=='@':break
  cursor=advance()
