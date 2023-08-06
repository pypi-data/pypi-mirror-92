import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lts-mpsjobtracker",
    version="0.0.15",
    author="Katie Amaral",
    author_email="kathryn_amaral@harvard.edu",
    description="A job tracker management module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.huit.harvard.edu/LTS/mps-job-tracker",
    packages=setuptools.find_packages(),
    install_requires=[
      'uuid',
      'jsonschema'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
      # Include all *.json files in any package
      "": ["*.json"],
    }
)