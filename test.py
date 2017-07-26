import ply.lex  as lex
import ply.yacc as yacc

tokens = ['SYM']

lex.lex()
yacc.yacc().parse(open('test.src').read())
