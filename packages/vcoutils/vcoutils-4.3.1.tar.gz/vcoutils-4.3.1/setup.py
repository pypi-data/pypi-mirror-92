import setuptools

MODULES = 4
CLASSES = 3
BUGFIX = 1

VERSION = f"{MODULES}.{CLASSES}.{BUGFIX}"

REQS = []

with open("README.md") as f:
    DESC = f.read()

setuptools.setup(
    name="vcoutils",
    author="vcokltfre",
    author_email="vcokltfre@gmail.com",
    version=VERSION,
    url="https://github.com/vcokltfre/vcoutils",
    packages=setuptools.find_packages(),
    description="A collection of utlities I have made or adapted for convenience.",
    long_description_content_type="text/markdown",
    long_description=DESC,
    install_requires=REQS
)