#!/usr/bin/env python

"""The setup script."""
import os
from setuptools import setup, find_packages

# with open('README.md', encoding='utf-8') as readme_file:
#     readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

setup_requirements = []

test_requirements = []

setup(
    author="Shamim Ferdous",
    author_email='shamimferdous5@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Generate and handle OTP or 2 step verifications easily and securely without using any DATABASES.",
    install_requires=requirements,
    license="MIT license",
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='py_cryptotp',
    name='py_cryptotp',
    packages=find_packages(include=['py_cryptotp', 'py_cryptotp.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shamimferdous/py_cryptotp',
    version='0.0.2',
    zip_safe=False,
)
