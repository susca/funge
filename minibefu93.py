#!/usr/bin/python3
# minibefu93.py -- a minimal Befunge93 interpreter written in Python
# usage: minibefu93.py <prog.fu>
import sys,random
o=sys.stdout
q=0,0
d=1,0
m=80,25
def k(x,y):return x+m[0]*y+y
def g(s,p=None):
  x,y=q if p is None else p
  return s[k(x,y)]
def p(s,p,v):
  o=k(*p)
  return s[:o]+chr(v)+s[o+1:]
def a():return (q[0]+d[0])%m[0],(q[1]+d[1])%m[1]
class S(list):
  def p(s,*a):return super().pop(*a) if s else 0
  def a(s,v):s.append(v)
  def __getitem__(s,key):return super().__getitem__(key) if s else 0
with open(sys.argv[1]) as f:r=f.read()
l=r.split('\n')
[l.append('') for _ in range(len(l),m[1])]
r='\n'.join(f'{s:<{m[0]}}' for s in l)
s=S()
f=False
while True:
  c=g(r)
  if c=='"':f=not f
  elif f:s.a(ord(c))
  elif c in '1234567890':s.a(int(c))
  elif c=='>':d=(1,0)
  elif c=='<':d=(-1,0)
  elif c=='^':d=(0,-1)
  elif c=='v':d=(0,1)
  elif c=='?':d=random.choice(((0,1),(1,0),(-1,0),(0,-1)))
  elif c=='#':q=a()
  elif c=='+':s.a(s.p()+s.p())
  elif c=='-':s.a(s.p(-2)-s.p())
  elif c=='*':s.a(s.p()*s.p())
  elif c=='/':s.a(int(s.p(-2) // s.p()))
  elif c=='%':s.a(s.p(-2) % s.p())
  elif c=='!':s.a(int(not bool(s.p())))
  elif c=='`':s.a(int(s.p(-2)>s.p()))
  elif c=='_':d=(-1,0) if s.p() else (1,0)
  elif c=='|':d=(0,-1) if s.p() else (0,1)
  elif c==':':s.a(s[-1])
  elif c=='\\':i,j=s.p(),s.p();s.a(i);s.a(j)
  elif c=='$':s.p()
  elif c=='.':o.write(str(s.p()));o.flush()
  elif c==',':o.write(chr(s.p()));o.flush()
  elif c=='&':s.a(int(input()))
  elif c=='~':s.a(ord(input()[0]))
  elif c=='g':y,x=s.p(),s.p();s.a(ord(g(r,(x,y))))
  elif c=='p':y,x,v=s.p(),s.p(),s.p();r=p(r,(x,y),v)
  elif c=='@':break
  q=a()
