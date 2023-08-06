from pip._internal.req import parse_requirements
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.requirement) for ir in reqs]


setup(
    name='usachev_pylint_checkers',
    version=0.1,
    author="Denis Usachev",
    author_email="usachevdy@yandex.ru",
    url="https://github.com/NightFantom/usachev_pylint_checkers",
    description='A library provides pylint checkers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src/', exclude=["dev_utils"]),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
    # install_requires=load_requirements("requirements.txt")
)
