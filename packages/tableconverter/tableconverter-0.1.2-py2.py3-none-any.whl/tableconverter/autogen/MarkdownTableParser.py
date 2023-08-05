# Generated from MarkdownTable.g4 by ANTLR 4.8
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\7")
        buf.write("8\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\4\3\4\3\4\6\4\32\n\4\r")
        buf.write("\4\16\4\33\3\4\3\4\3\5\3\5\3\5\7\5#\n\5\f\5\16\5&\13\5")
        buf.write("\3\5\3\5\5\5*\n\5\3\6\3\6\3\6\3\6\6\6\60\n\6\r\6\16\6")
        buf.write("\61\3\7\3\7\5\7\66\n\7\3\7\2\2\b\2\4\6\b\n\f\2\2\2\66")
        buf.write("\2\16\3\2\2\2\4\23\3\2\2\2\6\26\3\2\2\2\b$\3\2\2\2\n+")
        buf.write("\3\2\2\2\f\65\3\2\2\2\16\17\5\4\3\2\17\20\5\6\4\2\20\21")
        buf.write("\5\b\5\2\21\22\7\2\2\3\22\3\3\2\2\2\23\24\5\n\6\2\24\25")
        buf.write("\7\3\2\2\25\5\3\2\2\2\26\31\7\4\2\2\27\30\7\5\2\2\30\32")
        buf.write("\7\4\2\2\31\27\3\2\2\2\32\33\3\2\2\2\33\31\3\2\2\2\33")
        buf.write("\34\3\2\2\2\34\35\3\2\2\2\35\36\7\3\2\2\36\7\3\2\2\2\37")
        buf.write(" \5\n\6\2 !\7\3\2\2!#\3\2\2\2\"\37\3\2\2\2#&\3\2\2\2$")
        buf.write("\"\3\2\2\2$%\3\2\2\2%\'\3\2\2\2&$\3\2\2\2\')\5\n\6\2(")
        buf.write("*\7\3\2\2)(\3\2\2\2)*\3\2\2\2*\t\3\2\2\2+/\7\4\2\2,-\5")
        buf.write("\f\7\2-.\7\4\2\2.\60\3\2\2\2/,\3\2\2\2\60\61\3\2\2\2\61")
        buf.write("/\3\2\2\2\61\62\3\2\2\2\62\13\3\2\2\2\63\66\7\6\2\2\64")
        buf.write("\66\3\2\2\2\65\63\3\2\2\2\65\64\3\2\2\2\66\r\3\2\2\2\7")
        buf.write("\33$)\61\65")
        return buf.getvalue()


class MarkdownTableParser ( Parser ):

    grammarFileName = "MarkdownTable.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\n'", "'|'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "BAR", "STRING", 
                      "WS" ]

    RULE_table = 0
    RULE_header = 1
    RULE_sepLine = 2
    RULE_body = 3
    RULE_row = 4
    RULE_item = 5

    ruleNames =  [ "table", "header", "sepLine", "body", "row", "item" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    BAR=3
    STRING=4
    WS=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TableContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def header(self):
            return self.getTypedRuleContext(MarkdownTableParser.HeaderContext,0)


        def sepLine(self):
            return self.getTypedRuleContext(MarkdownTableParser.SepLineContext,0)


        def body(self):
            return self.getTypedRuleContext(MarkdownTableParser.BodyContext,0)


        def EOF(self):
            return self.getToken(MarkdownTableParser.EOF, 0)

        def getRuleIndex(self):
            return MarkdownTableParser.RULE_table

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTable" ):
                listener.enterTable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTable" ):
                listener.exitTable(self)




    def table(self):

        localctx = MarkdownTableParser.TableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_table)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.header()
            self.state = 13
            self.sepLine()
            self.state = 14
            self.body()
            self.state = 15
            self.match(MarkdownTableParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HeaderContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self):
            return self.getTypedRuleContext(MarkdownTableParser.RowContext,0)


        def getRuleIndex(self):
            return MarkdownTableParser.RULE_header

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHeader" ):
                listener.enterHeader(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHeader" ):
                listener.exitHeader(self)




    def header(self):

        localctx = MarkdownTableParser.HeaderContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_header)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.row()
            self.state = 18
            self.match(MarkdownTableParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SepLineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BAR(self, i:int=None):
            if i is None:
                return self.getTokens(MarkdownTableParser.BAR)
            else:
                return self.getToken(MarkdownTableParser.BAR, i)

        def getRuleIndex(self):
            return MarkdownTableParser.RULE_sepLine

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSepLine" ):
                listener.enterSepLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSepLine" ):
                listener.exitSepLine(self)




    def sepLine(self):

        localctx = MarkdownTableParser.SepLineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_sepLine)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(MarkdownTableParser.T__1)
            self.state = 23 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 21
                self.match(MarkdownTableParser.BAR)
                self.state = 22
                self.match(MarkdownTableParser.T__1)
                self.state = 25 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==MarkdownTableParser.BAR):
                    break

            self.state = 27
            self.match(MarkdownTableParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MarkdownTableParser.RowContext)
            else:
                return self.getTypedRuleContext(MarkdownTableParser.RowContext,i)


        def getRuleIndex(self):
            return MarkdownTableParser.RULE_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBody" ):
                listener.enterBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBody" ):
                listener.exitBody(self)




    def body(self):

        localctx = MarkdownTableParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 29
                    self.row()
                    self.state = 30
                    self.match(MarkdownTableParser.T__0) 
                self.state = 36
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

            self.state = 37
            self.row()
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==MarkdownTableParser.T__0:
                self.state = 38
                self.match(MarkdownTableParser.T__0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RowContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(MarkdownTableParser.ItemContext)
            else:
                return self.getTypedRuleContext(MarkdownTableParser.ItemContext,i)


        def getRuleIndex(self):
            return MarkdownTableParser.RULE_row

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRow" ):
                listener.enterRow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRow" ):
                listener.exitRow(self)




    def row(self):

        localctx = MarkdownTableParser.RowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_row)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self.match(MarkdownTableParser.T__1)
            self.state = 45 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 42
                self.item()
                self.state = 43
                self.match(MarkdownTableParser.T__1)
                self.state = 47 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==MarkdownTableParser.T__1 or _la==MarkdownTableParser.STRING):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ItemContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(MarkdownTableParser.STRING, 0)

        def getRuleIndex(self):
            return MarkdownTableParser.RULE_item

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterItem" ):
                listener.enterItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitItem" ):
                listener.exitItem(self)




    def item(self):

        localctx = MarkdownTableParser.ItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_item)
        try:
            self.state = 51
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [MarkdownTableParser.STRING]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.match(MarkdownTableParser.STRING)
                pass
            elif token in [MarkdownTableParser.T__1]:
                self.enterOuterAlt(localctx, 2)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





