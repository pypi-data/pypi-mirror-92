from os import path
import sys
from setuptools import setup, find_packages


setup(name = 'OpenRS',
    version = '0.0',
    description = 'Open Residual Stress analysis suite',
    long_description = 'https://github.com/majroy/OpenRS',
    url = 'https://github.com/majroy/OpenRS',
    author = 'M J Roy',
    author_email = 'matthew.roy@manchester.ac.uk',

    classifiers=[
        'Environment :: Win32 (MS Windows)',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        ],

    install_requires=['numpy'],
    license = 'Creative Commons Attribution-Noncommercial-Share Alike license',
    python_requires='>=3.8',

    )
