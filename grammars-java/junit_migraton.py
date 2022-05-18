import antlr4
from antlr4 import ParseTreeWalker, TokenStreamRewriter

from javagrammar.JavaLexer import JavaLexer
from javagrammar.JavaParserListener import JavaParserListener
from javagrammar.JavaParser import JavaParser

class JunitMigrationListener(JavaParserListener):

    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        print(ctx.getText())
        print(ctx.start.tokenIndex)
        print(ctx.stop.tokenIndex)
        pass

def __parse(code):
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    return tokens, parser.compilationUnit()
                
def main():
    code = open("./junit/src/test/java/com/example/project/JUnit4Test.java", "r").read()
    _, tree = __parse(code)
    listener = JunitMigrationListener()
    ParseTreeWalker().walk(listener, tree)

if __name__ == '__main__':
    main()