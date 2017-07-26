log = open('test.log','w')

### HGDB interfacing

from org.hypergraphdb import HyperGraph
# import org.hypergraphdb.atom.HGSubsumes
HyperGraph('db/test').close()

### core classes

class Sym:
    tag = 'sym'
    def __init__(self,V): self.val = V ; self.nest = []
    def __iadd__(self,o): self.nest.append(o) ; return self
    def __repr__(self): return self.dump()
    def dump(self, depth=0):
        S = '\n' + '\t' * depth + self.head()
        for i in self.nest: S += i.dump(depth + 1)
        return S
    def head(self): return '<%s:%s>'%(self.tag,self.val)
class Int(Sym):
    tag = 'int'
    def __init__(self,V): Sym.__init__(self, V) ; self.val = int(V)
class Num(Sym):
    tag = 'num'
    def __init__(self,V): Sym.__init__(self, V) ; self.val = float(V)
class Hex(Sym):
    tag = 'hex'
    def __init__(self,V): Sym.__init__(self, V) ; self.val = int(V,0x10)
    def head(self): return '<%s:0x%X>'%(self.tag,self.val)
class Bin(Sym):
    tag = 'bin'
    def __init__(self,V): Sym.__init__(self, V) ; self.val = int(V,0x02)
    def head(self): return '<%s:0b%s>'%(self.tag,'{0:b}'.format(self.val))
class Str(Sym):
    tag = 'str'
    def head(self): return '<%s:\'%s\'>'%(self.tag,self.val)

class Vector(Sym):
    tag = 'vector'
    def head(self): return '<%s:%s>'%(self.tag,len(self.nest))

class Op(Sym): tag = 'op'

### script interpreter

import ply.lex  as lex
import ply.yacc as yacc

### lexer

tokens = ['SYM','INT','NUM_p','NUM_i','HEX','BIN','STR',
          'LQ','RQ',
          'EQ']
states = (('str','exclusive'),)

t_ignore_COMMENT = r'\#.*'
t_ignore = ' \t\r'
def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
t_str_ignore = ''
def t_tick(t):
    r'\''
    t.lexer.push_state('str') ; t.lexer.str=''
def t_str_STR(t):
    r'\''
    t.lexer.pop_state() ; t.value = Str(t.lexer.str) ; return t
def t_str_chars(t):
    r'.'
    t.lexer.str += t.value

def t_HEX(t):
    r'0x[0-9A-Fa-f]+'
    t.value = Hex(t.value) ; return t
def t_BIN(t):
    r'0b[01]+'
    t.value = Bin(t.value) ; return t
def t_NUM_p(t):
    r'[\+\-]?[0-9]+\.[0-9]+([eE][\+\-]?[0-9]+)?'
    t.value = Num(t.value) ; return t
def t_NUM_i(t):
    r'[\+\-]?[0-9]+([eE][\+\-]?[0-9]+)'
    t.value = Num(t.value) ; return t
def t_INT(t):
    r'[\+\-]?[0-9]+'
    t.value = Int(t.value) ; return t

def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value) ; return t
    
def t_LQ(t):
    r'\['
    t.value = Op(t.value) ; return t
def t_RQ(t):
    r'\]'
    t.value = Op(t.value) ; return t

def t_EQ(t):
    r'\='
    t.value = Op(t.value) ; return t

## parser

def p_REPL_recur(p): ' REPL : '
def p_REPL(p):
    ' REPL : REPL ex '
    print >>log,p[2]
def p_ex_sym(p):
    ' ex : SYM '
    p[0] = p[1]
def p_ex_int(p):
    ' ex : INT '
    p[0] = p[1]
def p_ex_nump(p):
    ' ex : NUM_p '
    p[0] = p[1]
def p_ex_numi(p):
    ' ex : NUM_i '
    p[0] = p[1]
def p_ex_hex(p):
    ' ex : HEX '
    p[0] = p[1]
def p_ex_bin(p):
    ' ex : BIN '
    p[0] = p[1]
def p_ex_str(p):
    ' ex : STR '
    p[0] = p[1]

def p_ex_vector(p):
    ' ex : LQ vector RQ '
    p[0] = p[2]
    
def p_vector_none(p):
    ' vector : '
    p[0] = Vector('[]')
def p_vector_ex(p):
    ' vector : vector ex '
    p[0] = p[1] ; p[1] += p[2]

def p_ex_EQ(p):
    ' ex : ex EQ ex '
    p[0] = p[2] ; p[2] += p[1] ; p[2] += p[3]

## error callback

def t_ANY_error(t): raise BaseException('lexer:%s'%t)
def p_error(p): raise BaseException('parser:%s'%p)

## parser run

lex.lex()
yacc.yacc(debug=False,write_tables=False).parse(open('test.src').read())
