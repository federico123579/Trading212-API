from setuptools import setup, find_packages

from  lib.data import __VERSION__

setup(
    name="trading212api",
    version=__VERSION__,
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    author="Federico Lolli",
    author_email="federico123579@gmail.com",
    description="Package to interact with the broker service Trading212",
    license="MIT",
    keywords="trading api",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Emulators'
    ]
)