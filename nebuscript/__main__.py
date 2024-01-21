# TODO: Redo this betterer

import logging
from nebuscript.lexer import *

logger = logging.getLogger("NebuScript")
with open("example.nus", "r") as f:
    lexer = Lexer(f.read(), logger)

lexer.lex()

for token in lexer.tokens:
    print(token)