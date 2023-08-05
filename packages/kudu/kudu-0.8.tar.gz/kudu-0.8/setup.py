from setuptools import find_packages, setup

from kudu import __author__, __email__, __version__

setup(
    name='kudu',
    author=__author__,
    author_email=__email__,
    version=__version__,
    description='A deployment command line program in Python.',
    url='https://github.com/torfeld6/kudu',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='cli',
    packages=find_packages(),
    install_requires=[
        'click<8',
        'GitPython',
        'PyYAML',
        'requests>=2.20.1',
        'watchdog',
    ],
    entry_points={
        'console_scripts': [
            'kudu = kudu.__main__:cli',
        ],
    },
)
