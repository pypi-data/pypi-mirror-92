#!/usr/bin/env python
# coding: utf8
"""Setup.py for the EC2_COMPARE project."""

from pathlib import Path, PurePath
from setuptools import setup, find_packages
import sys
import os
import logging
from typing import Dict, Iterable, List

PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

PACKAGE_NAME = 'ec2_compare'
PACKAGE_VERSION = '1.0.0'

data_files = [
]

my_dir = PurePath(__file__).parent
try:
    with open(Path(my_dir/'README.md').resolve(), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

INSTALL_REQUIREMENTS: List[str] = []

default_requirements = [
    line
    for line in (Path(__file__).parent / "requirements.txt").read_text().split("\n")
    if line.strip() and not line.startswith("-")
]

git_requirements = [
    'gitpython'
]
devel_requirements = [
    line
    for line in (Path(__file__).parent / "requirements-dev.txt").read_text().split("\n")
    if line.strip() and not line.startswith("-")
]
if PY3:
    devel_requirements += ['mypy==0.790']
else:
    devel_requirements += ['unittest2']


if sys.version_info < (3, 2):
    INSTALL_REQUIREMENTS.append('futures')

EXTRAS_REQUIREMENTS: Dict[str, Iterable[str]] = {
    'devel': devel_requirements,
    'git': git_requirements,
}

def git_version(version_: str) -> str:
    """
    Return a version to identify the state of the underlying git repo.
    :param str version_: Semver version
    :return: Found version in Git repo or default
    :rtype: str
    """
    try:
        import git
        try:
            repo = git.Repo(Path(my_dir/'.git').resolve())
        except git.NoSuchPathError:
            logger.warning('.git directory not found: Cannot compute the git version')
            return PACKAGE_VERSION
        except git.InvalidGitRepositoryError:
            logger.warning('Invalid repo: Cannot compute the git version')
            return PACKAGE_VERSION
    except ImportError:
        logger.warning('gitpython module not found: Cannot compute the git version.')
        return PACKAGE_VERSION
    if repo:
        sha = repo.head.commit.hexsha
        if repo.is_dirty():
            return '.dirty:{version}+{sha}.dev0'.format(version=version_, sha=sha)
        return '.release:{version}+{sha}'.format(version=version_, sha=sha)
    return 'no_git_version:{version}'.format(version=version_)

def write_version(filename: str = 'version.txt'):
    """
    Write the Semver version + git hash to file, e.g. ".dev0+2b616650bc063e3eb93b16ab5492392ae954a5b6a5bd65e04bfcb9fead6f5682".
    :param str filename: Destination file to write
    """
    logger.info(str(Path(my_dir/'.git').resolve()))

    text = "{}".format(git_version(PACKAGE_VERSION))
    with open(filename, 'w') as file:
        file.write(text)
    return text

def do_setup():
    version_path = str(Path(my_dir/'version.txt').resolve())
    _version = os.environ.get('PACKAGE_VERSION', write_version(filename=version_path))
    if len(_version.split(":")) > 1:
        _version=_version.split(":")[1]
        if len(_version.split("+")) > 1:
            _version= _version.split("+")[0]

    version = "".join(e for e in _version if e.isalpha() or e.isnumeric() or e in ['.', '_','-'])

    setup(
        name=PACKAGE_NAME,
        version=version,
        long_description=long_description,
        long_description_content_type="text/markdown",
        author='Valeriys Soloviov',
        setup_requires=[
            'bowler',
            'docutils',
            'gitpython',
            'setuptools',
            'wheel',
        ],
        packages=find_packages(),
        install_requires=INSTALL_REQUIREMENTS,
        extras_require=EXTRAS_REQUIREMENTS,
    )
if __name__ == "__main__":
    do_setup()
