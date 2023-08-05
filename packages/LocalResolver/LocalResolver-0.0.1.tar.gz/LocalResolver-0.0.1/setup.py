from setuptools import setup, find_packages

setup(
    name = 'LocalResolver',
 
    version = "0.0.1",
    packages = find_packages(include=["LocalResolver"]),
    install_requires = ['scapy'],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package implement netbios and LLMNR query tool in python and HostnameResolver command line tool.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/LocalResolver',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ],
 
    entry_points = {
        'console_scripts': [
            'HostnameResolver = LocalResolver:resolve'
        ],
    },
    python_requires='>=3.6',
)
