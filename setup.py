"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="graphic_novel_pyarcade",
    version="0.1.0",  # Required
    description="Little framework to create a graphic novel with python arcade",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deangelisdf/graphic_novel_pyarcade",
    author="Domenico Francesco De Angelis",
    author_email="deangelis1993@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="graphic novel, game development, arcade",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["arcade"],
    extras_require={
        "dev": [],
        "test": [],
    },
    package_data={},
    entry_points={},
    project_urls={
        "Bug Reports": "https://github.com/deangelisdf/graphic_novel_pyarcade/issues",
        "Source": "https://github.com/deangelisdf/graphic_novel_pyarcade",
    },
)