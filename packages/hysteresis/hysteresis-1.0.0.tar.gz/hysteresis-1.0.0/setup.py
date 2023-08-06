import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hysteresis",
    version="1.0.0",
    author="Christian Slotboom",
    author_email="cslotboom@yahoo.com",
    description="Postprocessing tools for OpenSeesPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cslotboom/Hysteresis",
    packages=setuptools.find_packages(),
    # package_dir = {'': 'Hysteresis'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)