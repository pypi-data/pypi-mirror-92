import sys
from setuptools import setup, find_packages


def get_readme(name="README.md"):
    """Get readme file contents"""
    with open(name) as f:
        return f.read()


readme = get_readme()

requires = ["sardana", "redis", "msgpack", "msgpack_numpy"]

setup(
    name="sardana-streams",
    version="0.1.0",
    description="Distributed sardana recorder",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Jose Tiago Macara Coutinho",
    author_email="coutinhotiago@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    license="GPLv3",
    url="http://github.com/ALBA-Synchrotron/sardana-streams",
    project_urls={
        "Documentation": "https://github.com/ALBA-Synchrotron/sardana-streams",
        "Source": "https://github.com/ALBA-Synchrotron/sardana-streams",
    },
    packages=find_packages(),
    install_requires=requires,
    python_requires=">=3.5",
)
