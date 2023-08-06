import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytechecker", # Replace with your own username
    version="1.0.0",
    author="dcronqvist",
    author_email="daniel@dcronqvist.se",
    description="A lightweight type/object checking library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcronqvist/pytechecker",
    keywords="payload, api, type check, api payload, flask payload, flask, flask api, object check, check",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)