import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sciscripts",
    version="3.0.2",
    author="T Malfatti",
    author_email="malfatti@disroot.org",
    description="Scripts for controlling devices/running experiments/analyzing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/malfatti/SciScripts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.6',
)
