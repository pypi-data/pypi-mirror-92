import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsbb15_labs",
    version="0.0.1",
    author="Johan Edstedt",
    author_email="johan.edstedt@liu.se",
    description="Convenience functions for the tsbb15 labs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Parskatt/tsbb15_labs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
    python_requires='>=3.6',
)
