from setuptools import find_packages, setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name = 'unhashlib',
    version = '0.0.1',
    description = 'A string class enhancement',
    long_description = readme,
    #license = license,
    packages=find_packages(exclude=('tests', 'docs')),
    author = 'Roberto Reale',
    author_email = 'roberto@reale.me',
    url = 'https://github.com/reale/unhashlib',
    keywords = [ ],
    install_requires = [ ],
    test_suite = 'nose.collector',
    tests_require = ['nose'],
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
