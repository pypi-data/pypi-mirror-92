#!/usr/bin/env python
import setuptools
import re
import ciur


with open("README.rst") as file:
    LONG_DESCRIPTION = file.read()


def parse_requirements(filename, editable=False):
    _ = []
    for line in open(filename, "r"):
        if re.search("^\s*(#|-)", line):
            continue
        line = re.search("^\s*(.*)\s*", line).group(1)

        if not line:
            continue

        if not editable:
            m = re.search("#egg=(...*)", line)
            if m:
                line = m.group(1)

        m = re.search("(.+) #.*", line)
        if m:
            line = m.group(1)

        _.append(line)

    return _


EXTRA_REQUIRE = {
    'pdf': ["pdfminer==20140328"],  # TODO: exclude this from 3.6>
    # 'dev': ["pytest==6.2.1 "]
    'dev': parse_requirements("requirements-pip-dev.txt"),
}

setup_params = dict(
    name=ciur.__title__,
    description="Ciur is a scrapper layer based on DSL for extracting data",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    license="MIT",
    version=ciur.__version__,
    url=ciur.__git__,
    dependency_links=[
       "git+%s.git#egg=ciur" % ciur.__git__
    ],
    author_email=ciur.__email__,
    author=ciur.__author__,
    packages=[
        ciur.__title__
    ],
    install_requires=parse_requirements("requirements-pip.txt"),
    extras_require=EXTRA_REQUIRE,
    tests_require=['pytest'],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "ciur = ciur.cli:main",
        ]
    }
)


if __name__ == '__main__':
    setuptools.setup(**setup_params)
