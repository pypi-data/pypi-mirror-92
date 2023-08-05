from pversion import get_version
from setuptools import setup, find_packages

NAME = 'pversion'

DESCRIPTION = 'Retrieve a package version.'

LONG_DESCRIPTION = """
Retrieve the package version from a version file in the package root.
"""


setup(
    name=NAME,
    version=get_version(NAME),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
    url='https://github.com/sfneal/pversion',
    license='MIT',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
)
