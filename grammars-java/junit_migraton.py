import os
import sys
import antlr4
from antlr4 import ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from grammar.JavaLexer import JavaLexer
from grammar.JavaParserListener import JavaParserListener
from grammar.JavaParser import JavaParser
from junit import junit_listeners

def __parse(code):
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    return tokens, parser.compilationUnit()

def __migrate(project_path):
    for dirpath, _, files in os.walk(os.path.join(project_path, "src/test")):
            for file in files:
                src = open(os.path.join(dirpath, file), "r").read()
                tokens, tree = __parse(src)
                rewriter = TokenStreamRewriter(tokens)    
                default_listener = junit_listeners.DefaultListener(rewriter)
                ParseTreeWalker().walk(default_listener, tree)
                remainder_imports_listener = junit_listeners.ReminderImportsListener(rewriter, default_listener.remaining_imports)
                ParseTreeWalker().walk(remainder_imports_listener, tree)
                newcode = remainder_imports_listener.getParsedSourceAsText()
                print(newcode)
                __parse(newcode)

                
def main():
    project_path = sys.argv[1]
    __migrate(project_path)
    

if __name__ == '__main__':
    main()