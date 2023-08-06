from setuptools import setup, find_packages
import sys, os

version = '0.1.0a7'

def readfile(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        out = f.read()
    return out

desc = '\n'.join([readfile('README.rst'), readfile('CHANGELOG.rst')])

setup(name='morpcc',
      version=version,
      description="Morp Control Center",
      long_description=desc,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='framework cms',
      author='Izhar Firdaus',
      author_email='kagesenshi.87@gmail.com',
      url='http://github.com/morpframework/morpcc',
      license='GPLv3+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "morpfw>=0.4.0b4<0.5.0",
          "more.chameleon",
          "more.static",
          "deform",
          "alembic",
          "pygments",
          "html_sanitizer",
          "nltk",
          "luigi",
          'pycryptodome',
          'a_un',
          'timeago',
      ],
      entry_points={
      })
