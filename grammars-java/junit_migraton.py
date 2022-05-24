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
                
                
def main():
    code = open("./sample-app/src/test/java/com/example/project/JUnit4Test.java", "r").read()
    tokens, tree = __parse(code)
    rewriter = TokenStreamRewriter(tokens)    
    default_listener = junit_listeners.DefaultListener(rewriter)
    ParseTreeWalker().walk(default_listener, tree)
    remainder_imports_listener = junit_listeners.ReminderImportsListener(rewriter, default_listener.remaining_imports)
    ParseTreeWalker().walk(remainder_imports_listener, tree)
    newcode = remainder_imports_listener.getParsedSourceAsText()
    print(newcode)
    __parse(newcode)


if __name__ == '__main__':
    main()