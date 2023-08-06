import setuptools

VERSION = '0.0.1'
DESCRIPTION = "A package to parse chemical formulas"
LONG_DESCRIPTION = "A package to parse chemical formulas"

setuptools.setup(
    name="molecule-parser",
    version="0.0.1",
    author="Sebastien Eveno",
    author_email="sebastien.louis.eveno@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/SebastienEveno/molecule-parser",
    packages=setuptools.find_packages(),
    install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'chemical formula parser package'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)