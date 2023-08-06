# -*- coding: utf-8 -*-

from setuptools import setup
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('lyricsfetcher/lyricsfetcher.py').read(),
    re.M).group(1)

with open("./README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="lyrics-fetcher",
    packages=['lyricsfetcher'],
    entry_points={
        "console_scripts": ['fetch_lyrics = lyricsfetcher.lyricsfetcher:main']
    },
    py_modules=["lyricsfetcher"],
    include_package_data=True,
    package_data={'lyricsfetcher': ['outdir.conf', 'token.conf']},
    install_requires=[
        "lyricsgenius>=2.0.2",
        "docopt>=0.6"
    ],
    version=version,
    description="fetch lyrics from Genius using your command line",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["lyrics", "genius", "CLI"],
    license="GNU GPLv3",
    python_requires='>3.6',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: MacOS X",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
    ],
    author="Jelle Hubertse",
    url="https://github.com/JelleHubertse/lyrics-fetcher",
)
