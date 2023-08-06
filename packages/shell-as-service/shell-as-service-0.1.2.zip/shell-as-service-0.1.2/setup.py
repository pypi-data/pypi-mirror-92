import os

from setuptools import find_packages, setup

with open(os.path.join("version.txt")) as version_file:
    version_from_file = version_file.read().strip()

with open("test_requirements.txt") as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name="shell-as-service",
    packages=find_packages(),
    install_requires=[
        "jsonpickle",
    ],
    tests_require=required_for_tests,
    python_requires="~=3.7",
    version=version_from_file,
    package_data={"": ["*.txt"]},
    description="",
    include_package_data=True,
    entry_points={
        "console_scripts": ["shell-as-service = shell_as_service.server:main"]
    },
    extras_require={
        "client": [
            "bcrypt<3.2",
            "cryptography<3.3",
            "paramiko~=2.7.2",
            "requests",
            "cloudshell-shell-core",
            "docker",
        ],
        "server": [
            "flask",
            "xmltodict",
        ],
    },
)
