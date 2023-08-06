from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python-mitto-sdk",
    version="0.0.5",
    author="Justin Freels",
    author_email="justin@zuar.com",
    description="Python library to interact with Mitto's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfreels/python-mitto-sdk",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],
    extras_require={
        "dev": [
            "setuptools",
            "twine",
            "wheel",
            "python-dotenv"
        ]
    },
    python_requires='>=3.6',
)
