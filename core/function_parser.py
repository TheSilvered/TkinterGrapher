"""
Operator precedence:

num_literal: (0-9)+ ['.' (0-9)+]
one_arg_func_name: 'sin' | 'cos' | 'tan' | 'arcsin' | 'arccos' | 'arctan' | 'sqrt' | 'ln'
base_arg_func_name: 'rt' | 'log'

call_argument: '(' signed_expr ')' | implied_mul
one_arg_func_call: one_arg_func_name call_argument
base_arg_func_call: base_arg_func_name '_' value call_argument
literal: num_literal | 'pi' | 'e' | 'x' | func_call
value: literal | '(' signed_expr ')'
signed_value: ('+' | '-')? power
power: value ['^' value]
signed_power: signed_value ['^' value]
implied_mul: power [power]
signed_implied_mul: signed_power [power]
factor: power [('*' | '/') power]
signed_factor: signed_power [('*' | '/') power]
expr: factor [('+' | '-') factor]
signed_expr: signed_factor [('+' | '-') factor]
__root__: signed_expr
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from string import ascii_letters
import math

ONE_ARG_FUNCIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'arcsin': math.asin,
    'arccos': math.acos,
    'arctan': math.atan,
    'sqrt': math.sqrt,
    'ln': math.log
}

BASE_ARG_FUNCTIONS = {
    'rt': lambda num, index: num ** (1 / index),
    'log': math.log
}


class ParseFuncError:
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg


class TokenType(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    CARET = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    UNDERSCORE = auto()
    NUMBER = auto()
    IDENT = auto()

    EXPR_END = auto()

    @staticmethod
    def to_str(token_type):
        return Token.symbol_tok_to_str.get(token_type, str(token_type))


class Token:
    symbol_tok_from_str = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.STAR,
        '/': TokenType.SLASH,
        '^': TokenType.CARET,
        '(': TokenType.OPEN_PAREN,
        ')': TokenType.CLOSE_PAREN,
        '_': TokenType.UNDERSCORE
    }

    symbol_tok_to_str = {
        TokenType.PLUS: '+',
        TokenType.MINUS: '-',
        TokenType.STAR: '*',
        TokenType.SLASH: '/',
        TokenType.CARET: '^',
        TokenType.OPEN_PAREN: '(',
        TokenType.CLOSE_PAREN: ')',
        TokenType.UNDERSCORE: '_',
        TokenType.EXPR_END: 'Expression end'
    }

    def __init__(self, type_: TokenType, value=None):
        self.type = type_
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        elif isinstance(other, TokenType):
            return self.type == other
        elif isinstance(other, tuple):
            return self.type == other[0] and self.value == other[1]
        else:
            return NotImplemented

    def __repr__(self):
        if self.value is None:
            return f"Tok({self.type})"
        return f"Tok({self.type}, {self.value!r})"

    def __str__(self):
        if self.type in self.symbol_tok_to_str:
            return self.symbol_tok_to_str[self.type]
        elif self.type == TokenType.IDENT:
            return f"identifier {self.value!r}"
        elif self.type == TokenType.NUMBER:
            return f"number {self.value}"
        else:
            return repr(self)

    @staticmethod
    def from_str(symbol_str: str):
        if symbol_str not in Token.symbol_tok_from_str:
            return None
        return Token(Token.symbol_tok_from_str[symbol_str])


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.idx = 0

    def advance(self):
        self.idx += 1

    @property
    def c(self):
        if self.idx < len(self.text):
            return self.text[self.idx]
        return ''

    def tokenize(self) -> list[Token] | ParseFuncError:
        tokens = []

        while self.c:
            if self.c.isspace():
                self.advance()
            elif self.c in '0123456789':
                result = self.num_token()
                if isinstance(result, ParseFuncError):
                    return result
                tokens.append(result)
            elif self.c in ascii_letters:
                tokens.append(self.ident_token())
            else:
                result = self.symbol_token()
                if isinstance(result, ParseFuncError):
                    return result
                tokens.append(result)

        tokens.append(Token(TokenType.EXPR_END))
        return tokens

    def num_token(self) -> Token | ParseFuncError:
        num_str = ''

        while self.c and self.c in '0123456789 ':
            if self.c != ' ':
                num_str += self.c
            self.advance()

        if self.c != '.':
            return Token(TokenType.NUMBER, float(num_str))
        self.advance()

        if not self.c or self.c not in '0123456789':
            return ParseFuncError('expected a number after the dot')
        num_str += '.'
        while self.c and self.c in '0123456789 ':
            if self.c != ' ':
                num_str += self.c
            self.advance()
        return Token(TokenType.NUMBER, float(num_str))

    def ident_token(self) -> Token:
        name = ''
        while self.c and self.c in ascii_letters:
            name += self.c
            self.advance()
        return Token(TokenType.IDENT, name)

    def symbol_token(self) -> Token | ParseFuncError:
        token = Token.from_str(self.c)
        if token is None:
            return ParseFuncError(f"unexpected character '{self.c!r}'")
        self.advance()
        return token


class FuncAST(ABC):
    @abstractmethod
    def evaluate(self, x: float) -> float | None:
        pass

    def __repr__(self):
        attrs = list(self.__dict__.keys())
        attrs = [f"{attr}: {getattr(self, attr)}" for attr in attrs if not attr.startswith("__")]
        return self.__class__.__name__ + "(" + ", ".join(attrs) + ")"


class XNode(FuncAST):
    def evaluate(self, x: float) -> float | None:
        return x


class ValueNode(FuncAST):
    def __init__(self, value: float):
        self.value = value

    def evaluate(self, x: float) -> float | None:
        return self.value


class NegativeNode(FuncAST):
    def __init__(self, value_node: FuncAST):
        self.value_node = value_node

    def evaluate(self, x: float) -> float | None:
        result = self.value_node.evaluate(x)
        if result is None:
            return None
        return -result


class BinOpNode(FuncAST):
    def __init__(self, l_node: FuncAST, r_node: FuncAST, op: TokenType):
        self.l_node = l_node
        self.r_node = r_node
        self.op = op

    def evaluate(self, x: float) -> float | None:
        l_value = self.l_node.evaluate(x)
        if l_value is None:
            return None
        r_value = self.r_node.evaluate(x)
        if r_value is None:
            return None

        if self.op == TokenType.PLUS:
            return l_value + r_value
        elif self.op == TokenType.MINUS:
            return l_value - r_value
        elif self.op == TokenType.STAR:
            return l_value * r_value
        elif self.op == TokenType.SLASH:
            if r_value == 0:
                return None
            return l_value / r_value
        elif self.op == TokenType.CARET:
            if l_value == r_value == 0:
                return None
            result = l_value ** r_value
            if isinstance(result, complex):
                return None
            return result
        else:
            raise NotImplementedError(f"not implemented op {TokenType.to_str(self.op)!r}")


class OneArgCallNode(FuncAST):
    def __init__(self, value_node: FuncAST, func: str):
        self.value_node = value_node
        self.func = func

    def evaluate(self, x: float) -> float | None:
        value = self.value_node.evaluate(x)
        if value is None:
            return None

        func = ONE_ARG_FUNCIONS.get(self.func)
        if func is None:
            raise NotImplementedError(f"function {self.func!r} not implemented")
        try:
            return func(value)
        except (ZeroDivisionError, ValueError):
            return None
        except Exception as e:
            print(f"unhandled exception {e}")
            return None


class BaseArgCallNode(FuncAST):
    def __init__(self, value_node: FuncAST, base_node: FuncAST, func: str):
        self.value_node = value_node
        self.base_node = base_node
        self.func = func

    def evaluate(self, x: float) -> float | None:
        value = self.value_node.evaluate(x)
        if value is None:
            return None
        base = self.base_node.evaluate(x)
        if base is None:
            return None

        func = BASE_ARG_FUNCTIONS.get(self.func)
        if func is None:
            raise NotImplementedError(f"function {self.func!r} not implemented")
        try:
            return func(value, base)
        except (ZeroDivisionError, ValueError):
            return None
        except Exception as e:
            print(f"unhandled exception {e}")
            return None


class Parser:
    def __init__(self, tokens: list[Token], main_var: str):
        self.tokens = tokens
        self.main_var = main_var
        self.idx = 0

    def advance(self):
        self.idx += 1

    @property
    def tok(self) -> Token:
        return self.tokens[self.idx]

    def parse(self):
        expr = self.expr(True)
        if isinstance(expr, ParseFuncError):
            return expr
        if self.tok != TokenType.EXPR_END:
            return ParseFuncError(f"unexpected token {self.tok}")
        return expr

    def func_arg(self):
        if self.tok == TokenType.OPEN_PAREN:
            return self.value()
        else:
            return self.implied_mul(False)

    def literal(self):
        if self.tok == TokenType.NUMBER:
            node = ValueNode(self.tok.value)
            self.advance()
            return node
        elif self.tok == (TokenType.IDENT, self.main_var):
            self.advance()
            return XNode()
        elif self.tok == (TokenType.IDENT, 'pi'):
            self.advance()
            return ValueNode(math.pi)
        elif self.tok == (TokenType.IDENT, 'e'):
            self.advance()
            return ValueNode(math.e)
        elif self.tok == TokenType.IDENT and self.tok.value in ONE_ARG_FUNCIONS:
            func = self.tok.value
            self.advance()
            value_node = self.func_arg()
            if isinstance(value_node, ParseFuncError):
                return value_node
            return OneArgCallNode(value_node, func)
        elif self.tok == TokenType.IDENT and self.tok.value in BASE_ARG_FUNCTIONS:
            func = self.tok.value
            self.advance()
            if self.tok != TokenType.UNDERSCORE:
                return ParseFuncError(f"expected '_', fund {self.tok}")
            self.advance()
            base_node = self.value()
            if isinstance(base_node, ParseFuncError):
                return base_node
            value_node = self.func_arg()
            if isinstance(value_node, ParseFuncError):
                return value_node
            return BaseArgCallNode(value_node, base_node, func)
        else:
            return ParseFuncError(f"expected a value, found {self.tok}")

    def value(self):
        if self.tok == TokenType.OPEN_PAREN:
            self.advance()
            expr = self.expr(True)
            if self.tok != TokenType.CLOSE_PAREN:
                return ParseFuncError(f"expected ')', found {self.tok}")
            self.advance()
            return expr
        return self.literal()

    def signed_value(self):
        negative = False
        if self.tok == TokenType.PLUS:
            self.advance()
        elif self.tok == TokenType.MINUS:
            negative = True
            self.advance()
        value_node = self.power(False)
        if isinstance(value_node, ParseFuncError):
            return value_node
        if negative:
            return NegativeNode(value_node)
        else:
            return value_node

    def power(self, signed):
        if signed:
            l_node = self.signed_value()
        else:
            l_node = self.value()
        if isinstance(l_node, ParseFuncError):
            return l_node

        if self.tok != TokenType.CARET:
            return l_node
        self.advance()
        r_node = self.value()
        if isinstance(r_node, ParseFuncError):
            return r_node

        l_node = BinOpNode(l_node, r_node, TokenType.CARET)
        curr_node = l_node

        while self.tok == TokenType.CARET:
            self.advance()
            r_node = self.value()
            if isinstance(r_node, ParseFuncError):
                return r_node
            curr_node.r_node = BinOpNode(curr_node.r_node, r_node, TokenType.CARET)
            curr_node = curr_node.r_node

        return l_node

    def implied_mul(self, signed):
        l_node = self.power(signed)
        if isinstance(l_node, ParseFuncError):
            return l_node

        while True:
            idx = self.idx
            r_node = self.power(False)
            if isinstance(r_node, ParseFuncError):
                self.idx = idx
                return l_node
            l_node = BinOpNode(l_node, r_node, TokenType.STAR)

    def factor(self, signed):
        l_node = self.implied_mul(signed)
        if isinstance(l_node, ParseFuncError):
            return l_node

        while self.tok in (TokenType.STAR, TokenType.SLASH):
            op = self.tok.type
            self.advance()
            r_node = self.implied_mul(False)
            if isinstance(r_node, ParseFuncError):
                return r_node
            l_node = BinOpNode(l_node, r_node, op)

        return l_node

    def expr(self, signed):
        l_node = self.factor(signed)
        if isinstance(l_node, ParseFuncError):
            return l_node

        while self.tok in (TokenType.PLUS, TokenType.MINUS):
            op = self.tok.type
            self.advance()
            r_node = self.factor(False)
            if isinstance(r_node, ParseFuncError):
                return r_node
            l_node = BinOpNode(l_node, r_node, op)

        return l_node


def parse_func(func: str, main_var: str) -> ParseFuncError | FuncAST:
    lexer = Lexer(func)
    tokens = lexer.tokenize()

    if isinstance(tokens, ParseFuncError):
        return tokens

    parser = Parser(tokens, main_var)
    return parser.parse()
