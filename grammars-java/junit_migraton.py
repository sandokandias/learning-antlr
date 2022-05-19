from asyncore import readwrite
import antlr4
from antlr4 import ParseTreeWalker
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from javagrammar.JavaLexer import JavaLexer
from javagrammar.JavaParserListener import JavaParserListener
from javagrammar.JavaParser import JavaParser

class JunitMigrationListener(JavaParserListener):

    def __init__(self, rewriter: TokenStreamRewriter):
        self.rewriter = rewriter
        self.annotations = {
            "@Before": "@BeforeEach",
            "@After": "@AfterEach",
            "@BeforeClass": "@BeforeAll",
            "@AfterClass": "@AfterAll",
            "@Ignore": "@Disable"
        }
        self.imports = {
            "org.junit.After": "org.junit.jupiter.api.AfterEach",
            "org.junit.Before": "org.junit.jupiter.api.BeforeEach",
            "org.junit.AfterClass": "org.junit.jupiter.api.AfterAll",
            "org.junit.BeforeClass": "org.junit.jupiter.api.BeforeAll",
            "org.junit.Ignore": "org.junit.jupiter.api.Disable",
            "org.junit.Test": "org.junit.jupiter.api.Test",
            "org.junit.Assert.assertEquals": "org.junit.jupiter.api.Assertions.assertEquals"
        }

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
        elif annot in self.annotations:
            self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, self.annotations[annot])
    
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        for c in ctx.children:
            imp = c.getText()
            if imp in self.imports:
                self.rewriter.replaceRangeTokens(c.start, c.stop, self.imports[imp])


def __parse(code):
    lexer = JavaLexer(antlr4.InputStream(code))
    tokens = antlr4.CommonTokenStream(lexer)
    parser = JavaParser(tokens)
    return tokens, parser.compilationUnit()
                
def main():
    code = open("./junit/src/test/java/com/example/project/JUnit4Test.java", "r").read()
    tokens, tree = __parse(code)
    rewriter = TokenStreamRewriter(tokens)    
    listener = JunitMigrationListener(rewriter)
    ParseTreeWalker().walk(listener, tree)
    newcode = listener.rewriter.getDefaultText()
    print(newcode)
    __parse(newcode)


if __name__ == '__main__':
    main()