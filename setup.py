from setuptools import setup, find_packages

setup(
    name="trading212api",
    version="v0.2rc1",
    packages=find_packages(),
    install_requires=[
        'splinter',
        'pyvirtualdisplay',
        'bs4',
        'pyyaml'
    ],
    include_package_data=True,
    package_data={'': ['*.ini', 'logs/*.ini']},
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
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Emulators'
    ]
)
