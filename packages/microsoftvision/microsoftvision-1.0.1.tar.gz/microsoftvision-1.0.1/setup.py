import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setuptools.setup(
    name="microsoftvision",
    version="1.0.1",
    description="Downloads pretrained Microsoft Vision models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["torch>=1.2.0", "azure-storage-blob","azure-identity", "tqdm"],
)
