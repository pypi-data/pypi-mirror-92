from setuptools import find_packages, setup

setup(
    name='picoballoon',
    packages=find_packages(include=["picoballoon-api-lib"]),
    version='0.1.0',
    description='The API library for picoballoon',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Kalle Bracht',
    license='LICENSE',
    url="https://gitlab.com/picoballoon/python-api",
    install_requires=[
        "requests",
        "datetime",
        "typing"
    ],
)