# Generated from /home/omry/dev/hydra/hydra/grammar/OverrideParser.g4 by ANTLR 4.8
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\32")
        buf.write("\u00a0\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\4\17\t\17\3\2\3\2\3\2\5\2\"\n\2\3\2\3\2\3\2\3\2")
        buf.write("\5\2(\n\2\5\2*\n\2\3\2\3\2\3\2\3\2\5\2\60\n\2\5\2\62\n")
        buf.write("\2\3\2\3\2\3\3\3\3\3\3\5\39\n\3\3\4\3\4\3\4\3\4\6\4?\n")
        buf.write("\4\r\4\16\4@\5\4C\n\4\3\5\3\5\3\5\5\5H\n\5\3\6\3\6\5\6")
        buf.write("L\n\6\3\7\3\7\3\7\3\7\5\7R\n\7\3\b\3\b\3\b\6\bW\n\b\r")
        buf.write("\b\16\bX\3\t\3\t\3\t\3\n\3\n\3\n\5\na\n\n\3\n\3\n\3\n")
        buf.write("\5\nf\n\n\3\n\7\ni\n\n\f\n\16\nl\13\n\5\nn\n\n\3\n\3\n")
        buf.write("\3\13\3\13\3\13\3\13\7\13v\n\13\f\13\16\13y\13\13\5\13")
        buf.write("{\n\13\3\13\3\13\3\f\3\f\3\f\3\f\7\f\u0083\n\f\f\f\16")
        buf.write("\f\u0086\13\f\5\f\u0088\n\f\3\f\3\f\3\r\3\r\3\r\3\r\3")
        buf.write("\16\3\16\6\16\u0092\n\16\r\16\16\16\u0093\5\16\u0096\n")
        buf.write("\16\3\17\3\17\6\17\u009a\n\17\r\17\16\17\u009b\5\17\u009e")
        buf.write("\n\17\3\17\2\2\20\2\4\6\b\n\f\16\20\22\24\26\30\32\34")
        buf.write("\2\4\5\2\7\7\21\30\32\32\3\2\21\30\2\u00ad\2\61\3\2\2")
        buf.write("\2\4\65\3\2\2\2\6B\3\2\2\2\bG\3\2\2\2\nK\3\2\2\2\fQ\3")
        buf.write("\2\2\2\16S\3\2\2\2\20Z\3\2\2\2\22]\3\2\2\2\24q\3\2\2\2")
        buf.write("\26~\3\2\2\2\30\u008b\3\2\2\2\32\u0095\3\2\2\2\34\u009d")
        buf.write("\3\2\2\2\36\37\5\4\3\2\37!\7\3\2\2 \"\5\n\6\2! \3\2\2")
        buf.write("\2!\"\3\2\2\2\"\62\3\2\2\2#$\7\4\2\2$)\5\4\3\2%\'\7\3")
        buf.write("\2\2&(\5\n\6\2\'&\3\2\2\2\'(\3\2\2\2(*\3\2\2\2)%\3\2\2")
        buf.write("\2)*\3\2\2\2*\62\3\2\2\2+,\7\5\2\2,-\5\4\3\2-/\7\3\2\2")
        buf.write(".\60\5\n\6\2/.\3\2\2\2/\60\3\2\2\2\60\62\3\2\2\2\61\36")
        buf.write("\3\2\2\2\61#\3\2\2\2\61+\3\2\2\2\62\63\3\2\2\2\63\64\7")
        buf.write("\2\2\3\64\3\3\2\2\2\658\5\6\4\2\66\67\7\6\2\2\679\5\b")
        buf.write("\5\28\66\3\2\2\289\3\2\2\29\5\3\2\2\2:C\5\b\5\2;>\7\26")
        buf.write("\2\2<=\7\b\2\2=?\7\26\2\2><\3\2\2\2?@\3\2\2\2@>\3\2\2")
        buf.write("\2@A\3\2\2\2AC\3\2\2\2B:\3\2\2\2B;\3\2\2\2C\7\3\2\2\2")
        buf.write("DH\3\2\2\2EH\7\26\2\2FH\7\t\2\2GD\3\2\2\2GE\3\2\2\2GF")
        buf.write("\3\2\2\2H\t\3\2\2\2IL\5\f\7\2JL\5\16\b\2KI\3\2\2\2KJ\3")
        buf.write("\2\2\2L\13\3\2\2\2MR\5\32\16\2NR\5\24\13\2OR\5\26\f\2")
        buf.write("PR\5\22\n\2QM\3\2\2\2QN\3\2\2\2QO\3\2\2\2QP\3\2\2\2R\r")
        buf.write("\3\2\2\2SV\5\f\7\2TU\7\13\2\2UW\5\f\7\2VT\3\2\2\2WX\3")
        buf.write("\2\2\2XV\3\2\2\2XY\3\2\2\2Y\17\3\2\2\2Z[\7\26\2\2[\\\7")
        buf.write("\3\2\2\\\21\3\2\2\2]^\7\26\2\2^m\7\n\2\2_a\5\20\t\2`_")
        buf.write("\3\2\2\2`a\3\2\2\2ab\3\2\2\2bj\5\f\7\2ce\7\13\2\2df\5")
        buf.write("\20\t\2ed\3\2\2\2ef\3\2\2\2fg\3\2\2\2gi\5\f\7\2hc\3\2")
        buf.write("\2\2il\3\2\2\2jh\3\2\2\2jk\3\2\2\2kn\3\2\2\2lj\3\2\2\2")
        buf.write("m`\3\2\2\2mn\3\2\2\2no\3\2\2\2op\7\f\2\2p\23\3\2\2\2q")
        buf.write("z\7\r\2\2rw\5\f\7\2st\7\13\2\2tv\5\f\7\2us\3\2\2\2vy\3")
        buf.write("\2\2\2wu\3\2\2\2wx\3\2\2\2x{\3\2\2\2yw\3\2\2\2zr\3\2\2")
        buf.write("\2z{\3\2\2\2{|\3\2\2\2|}\7\16\2\2}\25\3\2\2\2~\u0087\7")
        buf.write("\17\2\2\177\u0084\5\30\r\2\u0080\u0081\7\13\2\2\u0081")
        buf.write("\u0083\5\30\r\2\u0082\u0080\3\2\2\2\u0083\u0086\3\2\2")
        buf.write("\2\u0084\u0082\3\2\2\2\u0084\u0085\3\2\2\2\u0085\u0088")
        buf.write("\3\2\2\2\u0086\u0084\3\2\2\2\u0087\177\3\2\2\2\u0087\u0088")
        buf.write("\3\2\2\2\u0088\u0089\3\2\2\2\u0089\u008a\7\20\2\2\u008a")
        buf.write("\27\3\2\2\2\u008b\u008c\5\34\17\2\u008c\u008d\7\7\2\2")
        buf.write("\u008d\u008e\5\f\7\2\u008e\31\3\2\2\2\u008f\u0096\7\31")
        buf.write("\2\2\u0090\u0092\t\2\2\2\u0091\u0090\3\2\2\2\u0092\u0093")
        buf.write("\3\2\2\2\u0093\u0091\3\2\2\2\u0093\u0094\3\2\2\2\u0094")
        buf.write("\u0096\3\2\2\2\u0095\u008f\3\2\2\2\u0095\u0091\3\2\2\2")
        buf.write("\u0096\33\3\2\2\2\u0097\u009e\7\31\2\2\u0098\u009a\t\3")
        buf.write("\2\2\u0099\u0098\3\2\2\2\u009a\u009b\3\2\2\2\u009b\u0099")
        buf.write("\3\2\2\2\u009b\u009c\3\2\2\2\u009c\u009e\3\2\2\2\u009d")
        buf.write("\u0097\3\2\2\2\u009d\u0099\3\2\2\2\u009e\35\3\2\2\2\32")
        buf.write("!\')/\618@BGKQX`ejmwz\u0084\u0087\u0093\u0095\u009b\u009d")
        return buf.getvalue()


class OverrideParser ( Parser ):

    grammarFileName = "OverrideParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "'~'", "'+'", "'@'", "':'", 
                     "'/'" ]

    symbolicNames = [ "<INVALID>", "EQUAL", "TILDE", "PLUS", "AT", "COLON", 
                      "SLASH", "DOT_PATH", "POPEN", "COMMA", "PCLOSE", "BRACKET_OPEN", 
                      "BRACKET_CLOSE", "BRACE_OPEN", "BRACE_CLOSE", "FLOAT", 
                      "INT", "BOOL", "NULL", "UNQUOTED_CHAR", "ID", "ESC", 
                      "WS", "QUOTED_VALUE", "INTERPOLATION" ]

    RULE_override = 0
    RULE_key = 1
    RULE_packageOrGroup = 2
    RULE_package = 3
    RULE_value = 4
    RULE_element = 5
    RULE_simpleChoiceSweep = 6
    RULE_argName = 7
    RULE_function = 8
    RULE_listContainer = 9
    RULE_dictContainer = 10
    RULE_dictKeyValuePair = 11
    RULE_primitive = 12
    RULE_dictKey = 13

    ruleNames =  [ "override", "key", "packageOrGroup", "package", "value", 
                   "element", "simpleChoiceSweep", "argName", "function", 
                   "listContainer", "dictContainer", "dictKeyValuePair", 
                   "primitive", "dictKey" ]

    EOF = Token.EOF
    EQUAL=1
    TILDE=2
    PLUS=3
    AT=4
    COLON=5
    SLASH=6
    DOT_PATH=7
    POPEN=8
    COMMA=9
    PCLOSE=10
    BRACKET_OPEN=11
    BRACKET_CLOSE=12
    BRACE_OPEN=13
    BRACE_CLOSE=14
    FLOAT=15
    INT=16
    BOOL=17
    NULL=18
    UNQUOTED_CHAR=19
    ID=20
    ESC=21
    WS=22
    QUOTED_VALUE=23
    INTERPOLATION=24

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.8")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class OverrideContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(OverrideParser.EOF, 0)

        def key(self):
            return self.getTypedRuleContext(OverrideParser.KeyContext,0)


        def EQUAL(self):
            return self.getToken(OverrideParser.EQUAL, 0)

        def TILDE(self):
            return self.getToken(OverrideParser.TILDE, 0)

        def PLUS(self):
            return self.getToken(OverrideParser.PLUS, 0)

        def value(self):
            return self.getTypedRuleContext(OverrideParser.ValueContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_override

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOverride" ):
                listener.enterOverride(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOverride" ):
                listener.exitOverride(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOverride" ):
                return visitor.visitOverride(self)
            else:
                return visitor.visitChildren(self)




    def override(self):

        localctx = OverrideParser.OverrideContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_override)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.EQUAL, OverrideParser.AT, OverrideParser.DOT_PATH, OverrideParser.ID]:
                self.state = 28
                self.key()
                self.state = 29
                self.match(OverrideParser.EQUAL)
                self.state = 31
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                    self.state = 30
                    self.value()


                pass
            elif token in [OverrideParser.TILDE]:
                self.state = 33
                self.match(OverrideParser.TILDE)
                self.state = 34
                self.key()
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==OverrideParser.EQUAL:
                    self.state = 35
                    self.match(OverrideParser.EQUAL)
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                        self.state = 36
                        self.value()




                pass
            elif token in [OverrideParser.PLUS]:
                self.state = 41
                self.match(OverrideParser.PLUS)
                self.state = 42
                self.key()
                self.state = 43
                self.match(OverrideParser.EQUAL)
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                    self.state = 44
                    self.value()


                pass
            else:
                raise NoViableAltException(self)

            self.state = 49
            self.match(OverrideParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class KeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def packageOrGroup(self):
            return self.getTypedRuleContext(OverrideParser.PackageOrGroupContext,0)


        def AT(self):
            return self.getToken(OverrideParser.AT, 0)

        def package(self):
            return self.getTypedRuleContext(OverrideParser.PackageContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_key

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterKey" ):
                listener.enterKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitKey" ):
                listener.exitKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitKey" ):
                return visitor.visitKey(self)
            else:
                return visitor.visitChildren(self)




    def key(self):

        localctx = OverrideParser.KeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_key)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.packageOrGroup()
            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==OverrideParser.AT:
                self.state = 52
                self.match(OverrideParser.AT)
                self.state = 53
                self.package()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PackageOrGroupContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def package(self):
            return self.getTypedRuleContext(OverrideParser.PackageContext,0)


        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.SLASH)
            else:
                return self.getToken(OverrideParser.SLASH, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_packageOrGroup

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPackageOrGroup" ):
                listener.enterPackageOrGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPackageOrGroup" ):
                listener.exitPackageOrGroup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPackageOrGroup" ):
                return visitor.visitPackageOrGroup(self)
            else:
                return visitor.visitChildren(self)




    def packageOrGroup(self):

        localctx = OverrideParser.PackageOrGroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_packageOrGroup)
        self._la = 0 # Token type
        try:
            self.state = 64
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.package()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.match(OverrideParser.ID)
                self.state = 60 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 58
                    self.match(OverrideParser.SLASH)
                    self.state = 59
                    self.match(OverrideParser.ID)
                    self.state = 62 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==OverrideParser.SLASH):
                        break

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PackageContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def DOT_PATH(self):
            return self.getToken(OverrideParser.DOT_PATH, 0)

        def getRuleIndex(self):
            return OverrideParser.RULE_package

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPackage" ):
                listener.enterPackage(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPackage" ):
                listener.exitPackage(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPackage" ):
                return visitor.visitPackage(self)
            else:
                return visitor.visitChildren(self)




    def package(self):

        localctx = OverrideParser.PackageContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_package)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.EOF, OverrideParser.EQUAL, OverrideParser.AT]:
                pass
            elif token in [OverrideParser.ID]:
                self.state = 67
                self.match(OverrideParser.ID)
                pass
            elif token in [OverrideParser.DOT_PATH]:
                self.state = 68
                self.match(OverrideParser.DOT_PATH)
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


    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self):
            return self.getTypedRuleContext(OverrideParser.ElementContext,0)


        def simpleChoiceSweep(self):
            return self.getTypedRuleContext(OverrideParser.SimpleChoiceSweepContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = OverrideParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 71
                self.element()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 72
                self.simpleChoiceSweep()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primitive(self):
            return self.getTypedRuleContext(OverrideParser.PrimitiveContext,0)


        def listContainer(self):
            return self.getTypedRuleContext(OverrideParser.ListContainerContext,0)


        def dictContainer(self):
            return self.getTypedRuleContext(OverrideParser.DictContainerContext,0)


        def function(self):
            return self.getTypedRuleContext(OverrideParser.FunctionContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElement" ):
                return visitor.visitElement(self)
            else:
                return visitor.visitChildren(self)




    def element(self):

        localctx = OverrideParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_element)
        try:
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 75
                self.primitive()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 76
                self.listContainer()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 77
                self.dictContainer()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 78
                self.function()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SimpleChoiceSweepContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_simpleChoiceSweep

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimpleChoiceSweep" ):
                listener.enterSimpleChoiceSweep(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimpleChoiceSweep" ):
                listener.exitSimpleChoiceSweep(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimpleChoiceSweep" ):
                return visitor.visitSimpleChoiceSweep(self)
            else:
                return visitor.visitChildren(self)




    def simpleChoiceSweep(self):

        localctx = OverrideParser.SimpleChoiceSweepContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_simpleChoiceSweep)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.element()
            self.state = 84 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 82
                self.match(OverrideParser.COMMA)
                self.state = 83
                self.element()
                self.state = 86 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==OverrideParser.COMMA):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgNameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def EQUAL(self):
            return self.getToken(OverrideParser.EQUAL, 0)

        def getRuleIndex(self):
            return OverrideParser.RULE_argName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgName" ):
                listener.enterArgName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgName" ):
                listener.exitArgName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgName" ):
                return visitor.visitArgName(self)
            else:
                return visitor.visitChildren(self)




    def argName(self):

        localctx = OverrideParser.ArgNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_argName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(OverrideParser.ID)
            self.state = 89
            self.match(OverrideParser.EQUAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(OverrideParser.ID, 0)

        def POPEN(self):
            return self.getToken(OverrideParser.POPEN, 0)

        def PCLOSE(self):
            return self.getToken(OverrideParser.PCLOSE, 0)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def argName(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ArgNameContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ArgNameContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)




    def function(self):

        localctx = OverrideParser.FunctionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_function)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(OverrideParser.ID)
            self.state = 92
            self.match(OverrideParser.POPEN)
            self.state = 107
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                self.state = 94
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,12,self._ctx)
                if la_ == 1:
                    self.state = 93
                    self.argName()


                self.state = 96
                self.element()
                self.state = 104
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 97
                    self.match(OverrideParser.COMMA)
                    self.state = 99
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
                    if la_ == 1:
                        self.state = 98
                        self.argName()


                    self.state = 101
                    self.element()
                    self.state = 106
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 109
            self.match(OverrideParser.PCLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContainerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACKET_OPEN(self):
            return self.getToken(OverrideParser.BRACKET_OPEN, 0)

        def BRACKET_CLOSE(self):
            return self.getToken(OverrideParser.BRACKET_CLOSE, 0)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.ElementContext)
            else:
                return self.getTypedRuleContext(OverrideParser.ElementContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_listContainer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterListContainer" ):
                listener.enterListContainer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitListContainer" ):
                listener.exitListContainer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitListContainer" ):
                return visitor.visitListContainer(self)
            else:
                return visitor.visitChildren(self)




    def listContainer(self):

        localctx = OverrideParser.ListContainerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_listContainer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 111
            self.match(OverrideParser.BRACKET_OPEN)
            self.state = 120
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.BRACKET_OPEN) | (1 << OverrideParser.BRACE_OPEN) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE) | (1 << OverrideParser.INTERPOLATION))) != 0):
                self.state = 112
                self.element()
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 113
                    self.match(OverrideParser.COMMA)
                    self.state = 114
                    self.element()
                    self.state = 119
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 122
            self.match(OverrideParser.BRACKET_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictContainerContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACE_OPEN(self):
            return self.getToken(OverrideParser.BRACE_OPEN, 0)

        def BRACE_CLOSE(self):
            return self.getToken(OverrideParser.BRACE_CLOSE, 0)

        def dictKeyValuePair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OverrideParser.DictKeyValuePairContext)
            else:
                return self.getTypedRuleContext(OverrideParser.DictKeyValuePairContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COMMA)
            else:
                return self.getToken(OverrideParser.COMMA, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_dictContainer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictContainer" ):
                listener.enterDictContainer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictContainer" ):
                listener.exitDictContainer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictContainer" ):
                return visitor.visitDictContainer(self)
            else:
                return visitor.visitChildren(self)




    def dictContainer(self):

        localctx = OverrideParser.DictContainerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_dictContainer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            self.match(OverrideParser.BRACE_OPEN)
            self.state = 133
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.QUOTED_VALUE))) != 0):
                self.state = 125
                self.dictKeyValuePair()
                self.state = 130
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==OverrideParser.COMMA:
                    self.state = 126
                    self.match(OverrideParser.COMMA)
                    self.state = 127
                    self.dictKeyValuePair()
                    self.state = 132
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 135
            self.match(OverrideParser.BRACE_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DictKeyValuePairContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def dictKey(self):
            return self.getTypedRuleContext(OverrideParser.DictKeyContext,0)


        def COLON(self):
            return self.getToken(OverrideParser.COLON, 0)

        def element(self):
            return self.getTypedRuleContext(OverrideParser.ElementContext,0)


        def getRuleIndex(self):
            return OverrideParser.RULE_dictKeyValuePair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictKeyValuePair" ):
                listener.enterDictKeyValuePair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictKeyValuePair" ):
                listener.exitDictKeyValuePair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictKeyValuePair" ):
                return visitor.visitDictKeyValuePair(self)
            else:
                return visitor.visitChildren(self)




    def dictKeyValuePair(self):

        localctx = OverrideParser.DictKeyValuePairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_dictKeyValuePair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.dictKey()
            self.state = 138
            self.match(OverrideParser.COLON)
            self.state = 139
            self.element()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimitiveContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_VALUE(self):
            return self.getToken(OverrideParser.QUOTED_VALUE, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def NULL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.NULL)
            else:
                return self.getToken(OverrideParser.NULL, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INT)
            else:
                return self.getToken(OverrideParser.INT, i)

        def FLOAT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.FLOAT)
            else:
                return self.getToken(OverrideParser.FLOAT, i)

        def BOOL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.BOOL)
            else:
                return self.getToken(OverrideParser.BOOL, i)

        def INTERPOLATION(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INTERPOLATION)
            else:
                return self.getToken(OverrideParser.INTERPOLATION, i)

        def UNQUOTED_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.UNQUOTED_CHAR)
            else:
                return self.getToken(OverrideParser.UNQUOTED_CHAR, i)

        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.COLON)
            else:
                return self.getToken(OverrideParser.COLON, i)

        def ESC(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ESC)
            else:
                return self.getToken(OverrideParser.ESC, i)

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.WS)
            else:
                return self.getToken(OverrideParser.WS, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_primitive

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimitive" ):
                listener.enterPrimitive(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimitive" ):
                listener.exitPrimitive(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimitive" ):
                return visitor.visitPrimitive(self)
            else:
                return visitor.visitChildren(self)




    def primitive(self):

        localctx = OverrideParser.PrimitiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_primitive)
        self._la = 0 # Token type
        try:
            self.state = 147
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.QUOTED_VALUE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 141
                self.match(OverrideParser.QUOTED_VALUE)
                pass
            elif token in [OverrideParser.COLON, OverrideParser.FLOAT, OverrideParser.INT, OverrideParser.BOOL, OverrideParser.NULL, OverrideParser.UNQUOTED_CHAR, OverrideParser.ID, OverrideParser.ESC, OverrideParser.WS, OverrideParser.INTERPOLATION]:
                self.enterOuterAlt(localctx, 2)
                self.state = 143 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 142
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.INTERPOLATION))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 145 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.COLON) | (1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS) | (1 << OverrideParser.INTERPOLATION))) != 0)):
                        break

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


    class DictKeyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUOTED_VALUE(self):
            return self.getToken(OverrideParser.QUOTED_VALUE, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ID)
            else:
                return self.getToken(OverrideParser.ID, i)

        def NULL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.NULL)
            else:
                return self.getToken(OverrideParser.NULL, i)

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.INT)
            else:
                return self.getToken(OverrideParser.INT, i)

        def FLOAT(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.FLOAT)
            else:
                return self.getToken(OverrideParser.FLOAT, i)

        def BOOL(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.BOOL)
            else:
                return self.getToken(OverrideParser.BOOL, i)

        def UNQUOTED_CHAR(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.UNQUOTED_CHAR)
            else:
                return self.getToken(OverrideParser.UNQUOTED_CHAR, i)

        def ESC(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.ESC)
            else:
                return self.getToken(OverrideParser.ESC, i)

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(OverrideParser.WS)
            else:
                return self.getToken(OverrideParser.WS, i)

        def getRuleIndex(self):
            return OverrideParser.RULE_dictKey

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDictKey" ):
                listener.enterDictKey(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDictKey" ):
                listener.exitDictKey(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDictKey" ):
                return visitor.visitDictKey(self)
            else:
                return visitor.visitChildren(self)




    def dictKey(self):

        localctx = OverrideParser.DictKeyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_dictKey)
        self._la = 0 # Token type
        try:
            self.state = 155
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OverrideParser.QUOTED_VALUE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 149
                self.match(OverrideParser.QUOTED_VALUE)
                pass
            elif token in [OverrideParser.FLOAT, OverrideParser.INT, OverrideParser.BOOL, OverrideParser.NULL, OverrideParser.UNQUOTED_CHAR, OverrideParser.ID, OverrideParser.ESC, OverrideParser.WS]:
                self.enterOuterAlt(localctx, 2)
                self.state = 151 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 150
                    _la = self._input.LA(1)
                    if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS))) != 0)):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 153 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OverrideParser.FLOAT) | (1 << OverrideParser.INT) | (1 << OverrideParser.BOOL) | (1 << OverrideParser.NULL) | (1 << OverrideParser.UNQUOTED_CHAR) | (1 << OverrideParser.ID) | (1 << OverrideParser.ESC) | (1 << OverrideParser.WS))) != 0)):
                        break

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





