# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sanetinel",
    version="0.1.9",
    author="Simon Rovder",
    author_email="simon.rovder@gmail.com",
    description="Algorithm monitoring by tracking variable value likelihoods.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sanetinel/python",
    packages=['sanetinel'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="GPL",
    python_requires='>=3.5',
    extras_require={
        'plotting': ['matplotlib']
    }
)
