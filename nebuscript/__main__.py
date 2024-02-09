# TODO: Redo this betterer

import logging
import sys
import argparse
import pathlib

from nebuscript.lexer import Lexer


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s |-| %(name)s |-| %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("NebuScript")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)


parser = argparse.ArgumentParser()
parser.add_argument("-V", "--verbose", action="store_true", help=argparse.SUPPRESS)
parser.add_argument("--developer", action="store_true", help=argparse.SUPPRESS)

subparser = parser.add_subparsers(dest="command")

build_parser = subparser.add_parser('build', help="Build NebuScript file.")
build_parser.add_argument("file")

args = parser.parse_args()

if args.verbose:
    handler.setLevel(logging.DEBUG)
    logger.info("Log Level set to 'DEBUG'")

if args.developer:
    logger.info("Created development folder")
    pathlib.Path("developer").mkdir(exist_ok=True)

match args.command:
    case "build":
        logger.info(f"Reading file: {args.file}")
        with open(args.file, "r") as file:
            lex = Lexer(file.read(), logger)
            file.close()
        logger.info(f"Finished reading file: {args.file}")
        tokens = lex.lex()
        if args.developer:
            logger.debug("Prepairing to write tokens...")
            with open("developer/tokens.txt", "w") as tokenList:
                for token in tokens:
                    tokenList.write(repr(token) + "\n")
                tokenList.close()
            logger.debug("Tokens have been written.")

    case None:
        parser.print_help()
