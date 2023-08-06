import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="benfords", # Replace with your own username
    version="1.0.1",
    author="Daniel McCarville",
    author_email="daniel.mccarville@gmail.com",
    description="Provides a series of functions to make Benford's Law usage more convenient.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielmccarville/Benfords",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
