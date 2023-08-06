import os
from setuptools import setup, find_packages

NAME = 'synfo'

DESCRIPTION = 'A lightweight utility for retrieving system information and specifications.'


def get_version(package_name, version_file='_version.py'):
    """
    Retrieve the package version from a version file in the package root.

    :param package_name:
    :param version_file: version file name (inside package root)
    :return: package version
    """
    filename = os.path.join(os.path.dirname(__file__), package_name, version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")


setup(name=NAME,
      version=get_version(NAME),
      packages=find_packages(),
      install_requires=[],
      entry_points={'console_scripts': ['synfo = synfo.system:main']},
      extras_require={'memory': 'psutil>=5.5.1'},
      url='https://github.com/sfneal/synfo',
      license='MIT',
      author='Stephen Neal',
      author_email='stephen@stephenneal.net',
      description=DESCRIPTION)
