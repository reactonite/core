from pathlib import Path

import setuptools

from reactonite import __version__ as version

REQUIREMENTS = Path("./requirements.txt").read_text()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reactonite",
    version=version,
    description="Transpile HTML to React",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SDOS2020/Team_3_Reactonite",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS
)
