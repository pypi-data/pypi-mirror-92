#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from shutil import copyfile
from os import chmod
import logging

logger = logging.getLogger()

with open("requirements.txt") as fp:
    install_requires = fp.readlines()


def _post_install(dir):
    logger.info("Copying executable to /usr/bin/pwdlearner")
    copyfile("__main__.py", "/usr/bin/pwdlearner")
    logger.info("Granting executable rights...")
    chmod("/usr/bin/pwdlearner", 0o755)
    logger.info("OK.")


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(
            _post_install, (self.install_lib,), msg="Running post install task"
        )


setup = install(
    setup(
        name="Password Learner",
        version="1.0",
        description="Password Learner Utility",
        author="Daniil Timachov",
        author_email="daniiltimachov@gmail.com",
        url="https://github.com/ghadd/password_learner",
        install_requires=install_requires,
        cmdclass={"install": install},
        packages=find_packages(),
    )
)
