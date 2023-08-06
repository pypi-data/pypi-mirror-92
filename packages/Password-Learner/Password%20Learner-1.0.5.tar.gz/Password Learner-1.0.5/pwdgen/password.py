
import jsonpickle
from clear_screen import clear
from countdown import countdown
from termcolor import colored

from typing import Dict


DEFAULT_PATH = "/tmp/lastpwd.obj"


class Password:
    MAX_PB_VALUE = 20
    LEARNED_PATH = "~/.pwdlearner/learned.obj"

    def __init__(self, size: int, config: Dict, contents: str):
        self.__size = size
        self.__config = config
        self.contents = contents
        self.progress = 0
        self.correct = 0
        self.last_attempt = "none"

    def save(self, learned=False):
        if learned:
            with open(self.LEARNED_PATH, "a") as file:
                file.write(self.contents + "\n")
        else:
            with open(DEFAULT_PATH, "w") as file:
                file.write(jsonpickle.dumps(self))

    @staticmethod
    def load():
        try:
            with open(DEFAULT_PATH, "r") as file:
                obj = jsonpickle.loads(file.read())
                return obj
        except IOError as e:
            raise IOError(
                "Could not load any password from previous sessions.")

    def __update_progress(self):
        self.correct = 0
        for i in range(min(len(self.last_attempt), self.__size)):
            if self.last_attempt[i] == self.contents[i]:
                self.correct += 1

        self.progress = (self.correct * self.MAX_PB_VALUE) // self.__size
        if self.correct == self.__size:
            self.save(learned=True)

    def __progressbar(self):
        print("[{}{}] ({}%)".format("#" * self.progress,
                                    " " * (self.MAX_PB_VALUE - self.progress),
                                    self.progress * 100 / self.__size))

    def __print_last_attempt(self):
        self.__update_progress()
        self.__progressbar()

    def learn(self):
        try:
            while True:
                self.__print_last_attempt()
                print("The password is: {}".format(
                    colored(self.contents, "green")))
                print("Your last attempt was: {}".format(
                    colored(self.last_attempt, "red")))
                try:
                    countdown(1)
                except KeyboardInterrupt:
                    pass
                clear()

                prompt = "Give in another try: " if self.correct == self.__size else "Polish it: "
                self.last_attempt = str(input(prompt))
                clear()
        except KeyboardInterrupt:
            clear()
            print(
                colored("Saving this password to renew in the next session...", "yellow"))
            self.save()
