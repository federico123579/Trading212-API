from setuptools import setup, find_packages

setup(
    name="trading212api",
    version="0.1b4",
    packages=['tradingAPI'],
    install_requires=[
        'splinter',
        'pyvirtualdisplay',
        'bs4'
    ],
    include_package_data=True,
    package_data={'': ['*.conf']},
    zip_safe=False,
    author="Federico Lolli",
    author_email="federico123579@gmail.com",
    description="Package to interact with the broker service Trading212",
    license="MIT",
    keywords="trading api",
    url="https://github.com/federico123579/Trading212-API",
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
