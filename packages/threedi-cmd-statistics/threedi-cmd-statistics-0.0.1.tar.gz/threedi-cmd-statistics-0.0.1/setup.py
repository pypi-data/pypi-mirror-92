#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "rich>=9.4.0",
    "typer>=0.3.2",
    "threedi-api-client>=3.0.21",
]

setup_requirements = [
    "pip>=20.3.3",
    "wheel>=0.33.6",
    "flake8>=3.7.8",
    "tox>=3.14.0",
    "coverage>=4.5.4",
    "twine>=1.14.0",
    "black>=20.8b1",
]

test_requirements = [ ]

setup(
    author="Lars Claussen",
    author_email='claussen.lars@nelen-schuurmans.nl',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Statistics plugin for the 3Di cmd client",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='threedi_api_stats',
    name='threedi-cmd-statistics',
    packages=find_packages(include=['threedi_cmd_statistics', 'threedi_cmd_statistics.*']),
    entry_points={
        "console_scripts": [
            "statistics=threedi_cmd_statistics.commands.statistics:main",
        ]
    },
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nens/threedi-cmd-statistics',
    version='0.0.1',
    zip_safe=False,
)
