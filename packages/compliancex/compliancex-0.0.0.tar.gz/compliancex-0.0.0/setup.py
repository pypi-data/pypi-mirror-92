import distutils.text_file
from pathlib import Path
from typing import List

import setuptools
from setuptools import setup,find_packages

from compliance.bcolor import *


def _parse_requirements(filename: str) -> List[str]:
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()


dep = _parse_requirements('requirements.txt')

print(f'{bcolors.OKGREEN} {dep} {bcolors.ENDC}')

setup(
    name='compliancex',
    version='0.0.0',
    install_requires=dep,
    packages=setuptools.find_packages(),
    py_modules=['module'],
    scripts=['compliance/cli.py']
)
