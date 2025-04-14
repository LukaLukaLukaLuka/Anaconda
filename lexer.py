#############
# VARIABLES #
#############
DIGITS = "0123456789"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_POWER = "POWER"


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name} : {self.details}"
        result += f"\nFile {self.pos_start.fn}, line {self.pos_start.line + 1}"
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Charachter", details)


class Position:
    def __init__(self, index, line, column, fn, ftx):
        self.index = index
        self.line = line
        self.column = column
        self.fn = fn
        self.ftx = ftx

    def advance(self, current_char):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 0
        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.fn, self.ftx)


class Token:  # Tokenizer
    def __init__(self, type_, value=None):  # define the vars
        self.type = type_
        self.value = value

    def __repr__(self):  # return the tokenized code
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:  # Lexer
    def __init__(self, fn, text):  # Define the vars
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.index] if self.pos.index < len(self.text) else None
        )

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TT_POWER))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
