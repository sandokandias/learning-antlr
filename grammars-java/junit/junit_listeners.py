from antlr4.TokenStreamRewriter import TokenStreamRewriter
from grammar.JavaParserListener import JavaParserListener
from grammar.JavaParser import JavaParser
from junit import junit

class DefaultListener(JavaParserListener):

    def __init__(self, rewriter: TokenStreamRewriter):
        self.rewriter = rewriter
        self.annotation_to_lambda = {
            "expected": ""
        }
        self.remaining_imports = {
            "expected": "",
            "timeout": ""
        }

    def enterAnnotation(self, ctx: JavaParser.AnnotationContext):
        annot = ctx.getText()
        if annot.startswith("@Test"):
            for c in ctx.children:
                    pair = c.getText().split("=")
                    if pair:
                        if pair[0] == "timeout":
                            self.remaining_imports["timeout"] = junit.imports["timeout"]
                            self.rewriter.insertAfterToken(ctx.stop, f"\n\t@Timeout({pair[1]})")
                        elif pair[0] == "expected":
                            self.annotation_to_lambda["expected"] = pair[1]
                            self.remaining_imports["expected"] = junit.imports["expected"]
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


class ReminderImportsListener(JavaParserListener):

    def __init__(self, rewriter: TokenStreamRewriter, remaining_imports: dict):
        self.__rewriter = rewriter
        self.remaining_imports = remaining_imports
        self.added_imports = {
            "expected": False,
            "timeout": False
        }

    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        for imp in self.remaining_imports:
            if not self.added_imports[imp]:
                self.__rewriter.insertAfterToken(ctx.stop, "\n" + self.remaining_imports[imp])
                self.added_imports[imp] = True
                break

    def getParsedSourceAsText(self):
        return self.__rewriter.getDefaultText()
