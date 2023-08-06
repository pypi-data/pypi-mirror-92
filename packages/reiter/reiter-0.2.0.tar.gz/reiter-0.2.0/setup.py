from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="reiter",
    version="0.2.0",
    packages=["reiter",],
    install_requires=[],
    license="MIT",
    url="https://github.com/lapets/reiter",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Wrapper for Python iterators and iterables that "+\
                "implements a list-like random-access interface.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
