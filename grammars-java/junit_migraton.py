from asyncore import readwrite
import antlr4
from antlr4 import ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from grammar.JavaLexer import JavaLexer
from grammar.JavaParserListener import JavaParserListener
from grammar.JavaParser import JavaParser
from junit import junit

class JunitMigrationListener(JavaParserListener):

    def __init__(self, rewriter: TokenStreamRewriter):
        self.rewriter = rewriter
        

    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        annot = ctx.getText()
        if annot.startswith("@Test"):
            for c in ctx.children:
                    pair = c.getText().split("=")
                    if pair:
                        if pair[0] == "timeout":
                            self.rewriter.insertBeforeToken(ctx.start, f"@Timeout({pair[1]})\n")
                            self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, "\t@Test")
                        elif pair[0] == "expected":
                            pass
        elif annot in junit.annotations:
            self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, junit.annotations[annot])
    
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        for c in ctx.children:
            imp = c.getText()
            if imp in junit.imports:
                self.rewriter.replaceRangeTokens(c.start, c.stop, junit.imports[imp])
    
    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        pass


def __parse(code):
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    return tokens, parser.compilationUnit()
                
def main():
    code = open("./sample-app/src/test/java/com/example/project/JUnit4Test.java", "r").read()
    tokens, tree = __parse(code)
    rewriter = TokenStreamRewriter(tokens)    
    listener = JunitMigrationListener(rewriter)
    ParseTreeWalker().walk(listener, tree)
    newcode = listener.rewriter.getDefaultText()
    print(newcode)
    __parse(newcode)


if __name__ == '__main__':
    main()