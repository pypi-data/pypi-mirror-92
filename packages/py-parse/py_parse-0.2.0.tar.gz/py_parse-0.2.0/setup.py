import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_parse",
    version="0.2.0",
    author="Lex Draven",
    author_email="lexman2@yandex.ru",
    description="A simplest HTML parsing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/kotolex/html_parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
