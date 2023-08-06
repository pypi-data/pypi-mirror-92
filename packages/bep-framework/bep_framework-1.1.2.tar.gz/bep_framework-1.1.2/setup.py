from setuptools import find_packages, setup

setup(
    name='bep_framework',
    packages=find_packages(include=['beplibrarylib']),
    version='1.1.2',
    description='Library for BEP',
    author='BEP',
    license='',
    install_requires=['psycopg2', 'flask', 'python-dateutil'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)