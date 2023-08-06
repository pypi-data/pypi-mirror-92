# Support functions for the labs in the TSBB15 course
## Installation
### Setup
Make sure you have python installed.
Additionally we recommend using a package manager such as [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Easiest installation
Run the command:
```terminal
pip install tsbb15-labs
```
Note that you do NOT need to clone this repo for this install.
### Install
If you want to change any code (bugfixes etc). You may want to install the package in editable mode, so that changes can be easily observed.
This can be done with the following commands:
```terminal
git clone git@github.com:Parskatt/tsbb15_labs.git
cd tsbb15_labs
pip install -e .
```

## Some known issues
### tiff errors
If you are using conda on windows you might get an error:
> tempfile.tif: Cannot read TIFF header.

If thats the case, uninstall libtiff (conda uninstall libtiff)
and reinstall it. (this will also require you to reinstall pillow)
