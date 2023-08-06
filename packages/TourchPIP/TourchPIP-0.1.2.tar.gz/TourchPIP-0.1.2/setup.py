import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.2'
PACKAGE_NAME = 'TourchPIP'
AUTHOR = ''
AUTHOR_EMAIL = ''
URL = 'https://github.com/Mostafa-ashraf19/TourchPIP'

LICENSE = 'MIT'
DESCRIPTION = 'DL Framework help you to build simple neural network'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'matplotlib',
      'requests'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      download_url='https://github.com/Mostafa-ashraf19/TourchPIP/archive/v_01.2.tar.gz'
      )
