#!/usr/bin/env python

from os import path
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from shutil import copyfile
from os import chmod
import logging

logger = logging.getLogger()

with open("requirements.txt") as fp:
    install_requires = fp.readlines()

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def _post_install(dir):
    logger.info("Copying executable to /usr/bin/pwdlearner")
    copyfile("pwdlearn/__main__.py", "/usr/bin/pwdlearner")
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
        version="1.0.5",
        description="Password Learner Utility",
        long_description=long_description,
        long_description_content_type='text/markdown',
        author="Daniil Timachov",
        author_email="daniiltimachov@gmail.com",
        url="https://github.com/ghadd/password_learner",
        install_requires=install_requires,
        cmdclass={"install": install},
        packages=find_packages(),
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ]
    )
)
