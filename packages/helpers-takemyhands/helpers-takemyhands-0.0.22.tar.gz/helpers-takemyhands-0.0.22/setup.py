from setuptools import setup, find_packages
from versioning import version

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

long_description = (
    open("README.md", "r", encoding="utf-8").read()
    + "\n\n"
    + open("NOTICES.txt", "r", encoding="utf-8").read()
)

setup(
    name="helpers-takemyhands",
    version=version,
    description="This help for python or django development easily.",
    long_description=long_description,
    author="TakeMyHands",
    author_email="wy0353@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keyword=[
        "helper",
        "helpers",
        "python",
        "django",
        "restframework",
        "takemyhands",
    ],
    packages=find_packages(),
    install_requires=[""],
)