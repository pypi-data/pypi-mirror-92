from setuptools import setup, find_packages

COMMAND_VERSION = "1.0.6"

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = ["boto3>=1.14.0", "docopt>=0.6.2", "termcolor>=1.1.0"]

setup(
    name="ssmpm",
    version=COMMAND_VERSION,
    author="Craig Hurley",
    author_email="craighurley78@gmail.com",
    license="MIT",
    description="SSM Parameter Manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/craighurley/ssmpm",
    packages=find_packages(),
    keywords="ssm, parameter, aws",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=install_requirements,
    python_requires=">=3.8",
    scripts=["bin/ssmpm"],
)
