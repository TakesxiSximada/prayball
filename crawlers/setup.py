#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import (
    setup,
    find_packages,
    )

here = os.path.abspath(os.path.dirname(__file__))
here_in = lambda path: os.path.join(here, path)


def get_requirements(path):
    with open(path) as fp:
        return list(map(lambda st: st.strip(), fp.readlines()))


setup(
    name='pray',
    version='0.1.0',
    url='https://github.com/TakesxiSximada/prayball',
    download_url='https://github.com/TakesxiSximada/prayball/archive/master.zip',
    license='See http://www.python.org/3.4/license.html',
    author='TakesxiSximada',
    author_email='takesxi.sxiamda@gmail.com',
    description="crawler",
    long_description="crawler",
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.4',
        ],
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=[
        ],
    package_data={},
    include_package_data=True,
    install_requires=get_requirements('requirements/install.txt'),
    test_require=get_requirements('requirements/test.txt'),
    entry_points='''
    [console_scripts]
    pray = pray.scripts:main
    '''
    )
