import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashmap_data_cataloger",  # Replace with your own username
    version="0.1.0.7",
    author="Hashmap, Inc",
    author_email="accelerators@hashmapinc.com",
    description="Early version of library - do not use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hashmapinc/oss/hashmap_data_cataloger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)