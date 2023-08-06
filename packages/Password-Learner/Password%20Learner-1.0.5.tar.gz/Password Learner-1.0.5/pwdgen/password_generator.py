

from pwdgen.password import Password
from typing import Dict, Union
import string
import random


class PasswordGenerator(object):
    __ambigous_chars = """({ } [ ] ( ) / \ ' " ` ~, ;: . < > )"""

    def __init__(self, size, **kwargs):
        """Constructor

        Args:
            size (int): size of the password (apparently 8 to 32 symbols)

            **allowed_chars (str)
                : string, containing all chars, which can be uses (does not set any filter, if not provided)
            **include_symbols (bool)
                : ( e.g. @#$% )
            **include_numbers (bool)
                : ( e.g. 123456 )
            **include_lowercase_chars (bool)
                : ( e.g. abcdefgh )
            **inlcude_uppercase_chars (bool)
                : ( e.g. ABCDEFGH )
            **exclude_ambigous_chars (bool)
                : ( { } [ ] ( ) / \ ' " ` ~ , ; : . < > )

        """
        self.size = size
        self.config = {
            "allowed_chars": self.__determine_kwarg(
                kwargs, "allowed_chars", None),

            "include_symbols": self.__determine_kwarg(
                kwargs, "include_symbols", True),
            "include_numbers": self.__determine_kwarg(
                kwargs, "include_numbers", True),
            "include_lowercase_chars": self.__determine_kwarg(
                kwargs, "inlcude_lowercase_chars", True),
            "include_uppercase_chars": self.__determine_kwarg(
                kwargs, "inlcude_upperacase_chars", True),
            "exclude_ambigous_chars": self.__determine_kwarg(
                kwargs, "exclude_ambigous_chars", False)
        }

        self.general_set = ""
        self._generate_general_set()

    @ staticmethod
    def __determine_kwarg(kwargs_dict: Dict, key: str, default: Union[bool, None]) -> Union[str, bool, None]:
        return kwargs_dict[key] if key in kwargs_dict else default

    def _generate_general_set(self):
        if self.config["allowed_chars"]:
            self.general_set = self.config["allowed_chars"]
            return

        if self.config["include_symbols"]:
            self.general_set += string.punctuation
        if self.config["include_numbers"]:
            self.general_set += string.digits
        if self.config["include_lowercase_chars"]:
            self.general_set += string.ascii_lowercase
        if self.config["include_uppercase_chars"]:
            self.general_set += string.ascii_uppercase
        if self.config["exclude_ambigous_chars"]:
            self.general_set = "".join(
                list(filter(lambda c: c in self.__ambigous_chars, self.general_set)))

    def generate(self) -> str:
        """This function generates a random passwords with previously set presets

        Returns:
            str: a generated password

        """
        if self.size < 8:
            raise ValueError("Passwords with length less than 8 are not safe.")
        elif self.size > 32:
            raise ValueError(
                "Passwords with length greater than 32 are not fully supported.")

        contents = "".join(random.sample(
            list(self.general_set * self.size), self.size))
        return Password(self.size, self.config, contents)
