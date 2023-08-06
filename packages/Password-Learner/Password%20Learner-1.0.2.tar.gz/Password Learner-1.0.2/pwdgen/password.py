
import jsonpickle
from clear_screen import clear
from countdown import countdown
from termcolor import colored

from typing import Dict


class Password:
    MAX_PB_VALUE = 20

    def __init__(self, size: int, config: Dict, contents: str):
        self.__size = size
        self.__config = config
        self.contents = contents
        self.progress = 0
        self.last_attempt = "none"

    def save(self):
        with open("/tmp/lastpwd.obj", "w") as file:
            file.write(jsonpickle.dumps(self))

    @staticmethod
    def load():
        try:
            with open("/tmp/lastpwd.obj", "r") as file:
                obj = jsonpickle.loads(file.read())
                return obj
        except IOError as e:
            raise IOError(
                "Could not load any password from previous sessions.")

    def __update_progress(self):
        correct = 0
        for i in range(min(len(self.last_attempt), self.__size)):
            if self.last_attempt[i] == self.contents[i]:
                correct += 1

        self.progress = (correct * self.MAX_PB_VALUE) // self.__size

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
                self.last_attempt = str(input("Give in another try:"))
                clear()
        except KeyboardInterrupt:
            clear()
            print(
                colored("Saving this password to renew in the next session...", "yellow"))
            self.save()
