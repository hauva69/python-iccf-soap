from setuptools import find_packages, setup

setup(
    name='iccf_xfcc',
    packages=find_packages(include=['iccf_xfcc']),
    version='0.1.0',
    description='Python library for the ICCF (xFCC Basic) SOAP API',
    author='Your Name',
    license='MIT',
    install_requires=['suds-community'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
