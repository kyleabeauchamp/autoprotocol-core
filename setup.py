from setuptools import setup, find_packages

setup(
    name = 'autoprotocol-core',
    version = '1.0.0',
    packages = find_packages(),
    license = 'MIT',
    long_description = open('README.md').read(),
    install_requires = ['autoprotocol==1.0.0'],
    test_suite="tests"
)
