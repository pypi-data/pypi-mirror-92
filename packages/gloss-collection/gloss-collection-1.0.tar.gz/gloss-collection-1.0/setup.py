from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="gloss-collection",
    version="1.0",
    author="Jeremiah Paige",
    author_email="ucodery@gmail.com",
    python_requires=">=3",
    packages=["gloss"],
    extras_require={
        "test": ["black", "flake8", "isort", "mypy", "pytest"],
        "dev": ["tox"],
    },
    url="https://github.com/ucodery/gloss",
    license="BSD",
    description="A synchronous one-to-one mapping type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dict map mapping collection gloss glossary translation",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
