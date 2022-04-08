import antlr4
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from JavaParser import JavaParser
from JavaLexer import JavaLexer
from JavaParserListener import JavaParserListener
from termcolor import colored, cprint

import sys

class AddFieldConstructorListener(JavaParserListener):

    def __init__(self, rewriter: TokenStreamRewriter):
        self.rewriter = rewriter
        self.snippet = {}
        self.__load_snippet()

    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        field = self.snippet["field"] + "\n"
        self.rewriter.insertAfter(ctx.start.tokenIndex + 1, field)

    def enterConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        constructor = self.snippet["constructor"].split("|")
        param = constructor[0]
        att = constructor[1] + "\n"
        self.rewriter.insertAfter(ctx.start.tokenIndex + 1, param)
        self.rewriter.insertAfter(ctx.stop.tokenIndex - 1, att)

    def __load_snippet(self):
        with open("java.code") as code:
            for line in code:
                key, val = line.partition("=")[::2]
                self.snippet[key.strip()] = val

        print(colored("snippet to inject:", "white", "on_blue"), end="\n")      
        print(colored(f"{self.snippet}", "white", "on_blue"), end="\n\n")

def __parse(code):
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    return tokens, parser.compilationUnit()
                
def main(args):
    file = args[1]
    code = open(file, 'r').read()
    print("====================Code====================", end="\n")
    print(colored(f"{code}", "blue", "on_white"), end="\n")      
    print("============================================", end="\n\n")

    print("                     ||                     ", end="\n")
    print("                     ||                     ", end="\n")
    print("                     ||                     ", end="\n")
    print("                     \/                     ", end="\n\n")

    tokens, tree = __parse(code)
    rewriter = TokenStreamRewriter(tokens)    
    listener = AddFieldConstructorListener(rewriter)
    ParseTreeWalker().walk(listener, tree)
    newcode = listener.rewriter.getDefaultText()

    print("==============Transformed Code==============", end="\n")
    print(colored(f"{newcode}", "blue", "on_white"), end="\n")      
    print("============================================", end="\n\n")

    __parse(newcode)

    
if __name__ == '__main__':
    main(sys.argv)
