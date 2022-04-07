import antlr4
from antlr4 import *
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from JavaParser import JavaParser
from JavaLexer import JavaLexer
from JavaParserListener import JavaParserListener

class AddFieldConstructorListener(JavaParserListener):

    # need parser to extract token stream
    def __init__(self, rewriter: TokenStreamRewriter):
        self.rewriter = rewriter

    def enterClassBody(self, ctx: JavaParser.ClassBodyContext):
        field = "public final String password;\n"
        self.rewriter.insertAfter(ctx.start.tokenIndex + 1, field)

    def enterConstructorDeclaration(self, ctx:JavaParser.ConstructorDeclarationContext):
        param = "String password, "
        att = "\tthis.password = password;\n"
        self.rewriter.insertAfter(ctx.start.tokenIndex + 1, param)
        self.rewriter.insertAfter(ctx.stop.tokenIndex - 1, att)
   
                
def main():
    code = open("User.java", 'r').read()
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    tree = parser.compilationUnit()
    rewriter = TokenStreamRewriter(tokens)    
    listener = AddFieldConstructorListener(rewriter)
    ParseTreeWalker().walk(listener, tree)
    print(listener.rewriter.getDefaultText())

    
if __name__ == '__main__':
    main()
