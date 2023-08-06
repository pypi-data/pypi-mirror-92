import setuptools

with open("README4PyPI.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="webdriver-update-tool",
    version="0.1.2",
    author="cjz25",
    description="A tool for updating the webdriver automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    install_requires=[
        'selenium >= 3.141.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.5',
)
