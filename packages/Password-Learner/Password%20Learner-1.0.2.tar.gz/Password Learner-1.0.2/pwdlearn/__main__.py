#!/usr/bin/env python

from pwdgen.password import Password
from pwdgen import PasswordGenerator as PGen

from argparse import ArgumentParser

parser = ArgumentParser(description="Learn passwords!")
parser.add_argument("--new", action="store_true", dest="create_new")
parser.add_argument("--allowed-chars", dest="allowed_chars", default=None)
parser.add_argument(
    "-e", "--exclude-ambigous", dest="exclude_ambigous_chars", action="store_true"
)
parser.add_argument("-l", "--length", dest="length", default=16)


if __name__ == "__main__":
    args = parser.parse_args()

    if not args.create_new:
        try:
            pwd = Password.load()
            pwd.learn()
        except IOError:
            pass

    gen = PGen(
        args.length,
        allowed_chars=args.allowed_chars,
        exclude_ambigous_chars=args.exclude_ambigous_chars,
    )
    pwd = gen.generate()

    pwd.learn()
