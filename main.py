import sys
from antlr4 import *
from NajaLexer import NajaLexer
from NajaParser import NajaParser
from rewriter import RewriteListener

def main(argv):
    input = FileStream(argv[1])
    lexer = NajaLexer(input)
    stream = CommonTokenStream(lexer)
    parser = NajaParser(stream)
    tree = parser.prog()

    walker = ParseTreeWalker()
    walker.walk(RewriteListener(), tree)
    print("Compilado com sucesso")

if __name__ == '__main__':
    main(sys.argv)
