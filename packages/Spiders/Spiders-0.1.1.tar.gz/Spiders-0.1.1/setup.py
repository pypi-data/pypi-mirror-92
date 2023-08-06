from setuptools import setup, find_packages


setup(
    name="Spiders",
    version="0.1.1",
    author="mr-josh",
    author_email="mr-josh@sparklapse.com",
    url="https://github.com/Sparklapse/Spiders",
    description="Asynchronous python server",
    long_description=open("./docs/README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
)
