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
        self.annotation_to_lambda = {
            "expected": ""
        }

    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        annot = ctx.getText()
        if annot.startswith("@Test"):
            for c in ctx.children:
                    pair = c.getText().split("=")
                    if pair:
                        if pair[0] == "timeout":
                            self.rewriter.insertAfterToken(ctx.stop, f"\n\t@Timeout({pair[1]})")
                        elif pair[0] == "expected":
                            self.annotation_to_lambda["expected"] = pair[1]
                        self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, "@Test")

        elif annot in junit.annotations:
            self.rewriter.replaceRangeTokens(ctx.start, ctx.stop, junit.annotations[annot])
    
    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        for c in ctx.children:
            imp = c.getText()
            if imp in junit.imports:
                self.rewriter.replaceRangeTokens(c.start, c.stop, junit.imports[imp])
    
    def enterMethodBody(self, ctx: JavaParser.MethodBodyContext):
        if self.annotation_to_lambda["expected"]:
            expected_except = self.annotation_to_lambda["expected"]
            start_lambda = junit.expected_lambda[1].replace("@exception", expected_except)
            end_lambda = junit.expected_lambda[2]
            self.rewriter.insertAfter(ctx.start.tokenIndex + 1, "\t")
            self.rewriter.insertAfterToken(ctx.start, start_lambda)
            self.rewriter.insertBeforeToken(ctx.stop, end_lambda)
            self.annotation_to_lambda["expected"] = ""


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