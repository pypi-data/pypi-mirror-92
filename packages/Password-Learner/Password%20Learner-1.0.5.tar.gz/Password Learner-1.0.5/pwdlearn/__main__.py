#!/usr/bin/env python

from pwdgen.password import Password
from pwdgen import PasswordGenerator as PGen

from argparse import ArgumentParser
from termcolor import colored
from pathlib import Path

parser = ArgumentParser(description="Learn passwords!")
parser.add_argument("--new", action="store_true", dest="create_new")
parser.add_argument("--allowed-chars", dest="allowed_chars", default=None)
parser.add_argument(
    "-e", "--exclude-ambigous", dest="exclude_ambigous_chars", action="store_true"
)
parser.add_argument("-l", "--length", dest="length", default=16)


if __name__ == "__main__":
    Path("~/.pwdlearner").mkdir(parents=True, exist_ok=True)
    args = parser.parse_args()

    if not args.create_new:
        try:
            pwd = Password.load()
        except IOError:
            print("Please, specify tag --new to create a new password.")
            exit(1)
    else:
        try:
            gen = PGen(
                int(args.length),
                allowed_chars=args.allowed_chars,
                exclude_ambigous_chars=args.exclude_ambigous_chars,
            )
        except ValueError as e:
            print(colored(e, "red"))
            exit(1)

        pwd = gen.generate()

    pwd.learn()
