import sys

from nebuscript.Token import *
import logging


class Lexer:
    def __init__(self, input, logger):
        self.source = input + "\n"
        self.curChar = ''
        self.curPos = -1
        self.tokens = []
        self.logger: logging.Logger = logger
        self.logger.info("Initializing lexer...")

        self.curLine = 1
        self.curColumn = 0

        self.nextChar()

    def nextChar(self):
        self.curColumn += 1
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    def abort(self, message):
        # TODO: Change to Exception Manager
        self.logger.critical(f"Lexing error: {message} @ {self.curLine}:{self.curColumn}")
        sys.exit(1)

    def getToken(self):
        self.skipWhitespace()
        self.skipComment()

        token = None

        if self.curChar == "\0":
            token = Token(TokenType.EOF, "", self.curLine, self.curColumn)
        elif self.curChar == '\n':
            token = Token(TokenType.NEWLINE, "", self.curLine, self.curColumn)
            self.curLine += 1
            self.curColumn = 0

        elif self.curChar == '-':
            if self.peek() == '>':
                self.nextChar()
                token = Token(TokenType.TYPEOF, "->", self.curLine, self.curColumn)
            else:
                token = Token(TokenType.MINUS, "-", self.curLine, self.curColumn)


        elif self.curChar == '=':
            if self.peek() == '=':
                self.nextChar()
                token = Token(TokenType.EQUALS, "==", self.curLine, self.curColumn)
            else:
                token = Token(TokenType.EQUALS, "=", self.curLine, self.curColumn)

        elif self.curChar == ';':
            token = Token(TokenType.EOL, ";", self.curLine, self.curColumn)

        elif self.curChar == '(':
            token = Token(TokenType.LPAREN, "(", self.curLine, self.curColumn)

        elif self.curChar == ')':
            token = Token(TokenType.RPAREN, ")", self.curLine, self.curColumn)

        elif self.curChar == '{':
            token = Token(TokenType.LBRACE, "{", self.curLine, self.curColumn)

        elif self.curChar == '}':
            token = Token(TokenType.RBRACE, "}", self.curLine, self.curColumn)

        elif self.curChar == '[':
            token = Token(TokenType.LSQUARE, "[", self.curLine, self.curColumn)

        elif self.curChar == ']':
            token = Token(TokenType.RSQUARE, "]", self.curLine, self.curColumn)

        elif self.curChar == ',':
            token = Token(TokenType.COMA, ",", self.curLine, self.curColumn)

        elif self.curChar == '>':
            token = Token(TokenType.MORETHAN, ">", self.curLine, self.curColumn)

        elif self.curChar == '<':
            token = Token(TokenType.LESSTHAN, "<", self.curLine, self.curColumn)

        elif self.curChar == '+':
            token = Token(TokenType.PLUS, "+", self.curLine, self.curColumn)

        elif self.curChar == '*':
            token = Token(TokenType.MULTIPLY, "*", self.curLine, self.curColumn)

        elif self.curChar == '/':
            token = Token(TokenType.DIVIDE, "/", self.curLine, self.curColumn)

        elif self.curChar == 'enum':
            token = Token(TokenType.ENUM, "enum", self.curLine, self.curColumn)

        elif self.curChar == 'struct':
            token = Token(TokenType.STRUCT, "struct", self.curLine, self.curColumn)

        elif self.curChar == ':':
            token = Token(TokenType.COLON, ":", self.curLine, self.curColumn)

        elif self.curChar == '.':
            token = Token(TokenType.DOT, ".", self.curLine, self.curColumn)

        elif self.curChar == '!':
            token = Token(TokenType.FEATURE, ".", self.curLine, self.curColumn)

        elif self.curChar == '\"':
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos: self.curPos]  # Get the substring.
            token = Token(TokenType.STRING, tokText, self.curLine, self.curColumn)

        elif self.curChar.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            startPos = self.curPos
            decimal = False
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':  # Decimal!
                decimal = True
                self.nextChar()

                # Must have at least one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos: self.curPos + 1]  # Get the substring.
            if decimal:
                token = Token(TokenType.FLOAT, tokText, self.curLine, self.curColumn)
            else:
                token = Token(TokenType.INT, tokText, self.curLine, self.curColumn)

        elif self.curChar.isalpha():
            startPos = self.curPos

            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos: self.curPos + 1]  # Get the substring.
            keyword = Token.checkIfKeyword(tokText)
            flipType = Token.checkIfType(tokText)

            if flipType:
                token = Token(flipType, tokText, self.curLine, self.curColumn)
            elif keyword:  # Keyword
                token = Token(keyword, tokText, self.curLine, self.curColumn)
            else:
                token = Token(TokenType.IDENTIFIER, tokText, self.curLine, self.curColumn)
        else:
            self.abort("Unrecognized character: " + self.curChar)

        self.nextChar()
        self.logger.debug("Recieved new token: " + str(token))
        return token

    def skipWhitespace(self):
        self.logger.debug("Skipping whitespace")
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        self.logger.debug("Skipping comment")
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()


    def lex(self):
        self.logger.info("Beginning Lexing")
        self.tokens = []

        while True:
            token = self.getToken()

            if token.type == TokenType.EOF:
                break

            self.tokens.append(token)
        self.tokens.append(Token(TokenType.EOF, "", self.curLine, self.curColumn))

        self.logger.info(f"Lexing complete. {len(self.tokens)} tokens found.")
        return self.tokens
