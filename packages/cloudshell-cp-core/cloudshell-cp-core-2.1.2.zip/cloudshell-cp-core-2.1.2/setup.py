import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("requirements.txt") as f_required:
    required = f_required.read().splitlines()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="cloudshell-cp-core",
    url="http://www.qualisystems.com/",
    author="Quali",
    author_email="info@quali.com",
    packages=find_packages(),
    install_requires=required,
    python_requires="~=3.7",
    tests_require=required_for_tests,
    test_suite="nose.collector",
    version=version_from_file,
    description=(
        "A repository for projects providing out of the box capabilities within "
        "CloudShell to parse and convert cloudShell driver request to well defined "
        "python objects. One cloudshell-cp-core For All cloudshell cloud provider "
        "shells."
    ),
    keywords="sandbox cloudshell json request",
    include_package_data=True,
)
