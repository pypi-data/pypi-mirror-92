from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="tellweather",
    version="1.1",
    description="A Python package to get weather reports for any location.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mantej1995/Upwork/tree/main/upwork/tellweather",
    author="Mantej Singh",
    author_email="mantejsgill@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["tellweather"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "tellweather=tellweather.cli:main",
        ]
    },
)