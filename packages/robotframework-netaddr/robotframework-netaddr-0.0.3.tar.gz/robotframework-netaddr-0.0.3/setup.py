# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().split("\n")


setup(
    name = "robotframework-netaddr",
    version = "0.0.2",
    author = "Niels Keulen",
    author_email = "nkeulen@gmail.com",
    description = "Robotframework keyword for the python netaddr library",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/nkeulen/robotframework-netaddr",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Library",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance"
    ],
    keywords = "netaddr, robotframework, ip address, ipv4, ipv6, mac address, network",
    install_requires = requirements,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    include_package_data=True
)
