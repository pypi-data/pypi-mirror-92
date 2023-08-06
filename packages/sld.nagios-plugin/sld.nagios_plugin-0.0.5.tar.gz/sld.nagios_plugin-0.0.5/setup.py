#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Matthew Larsen",
    author_email='Matt Larsen <matt.larsen@connorgp.com>',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Library to implement the Nagios Core Plugin API",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='nagios plugin',
    name='sld.nagios_plugin',
    packages=find_packages(include=['nagios_plugin', 'nagios_plugin.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SoldenServices/python-nagios-plugin',
    version='0.0.5',
    zip_safe=False,
)
