# DCIC-wrangling

This is a collection of scripts and Jupyter notebooks that can be helpful when performing many data wrangling tasks.  Most of the tools are specific to 4DN Nucleome wrangling needs, however may be modified to be more generally useful for certain tasks.

## Install

Packaged with `poetry` can be installed using `make`, `poetry` or `pip`.

From the dcicwrangling directory - `make build`

If you already have poetry installed - `poetry install`

Or to pip install from PyPi - `pip install dcicwrangling`

All dependencies are installed by default - if for some reason you don't want to install `pytest` packages or `invoke` (used to launch notebooks) you can do `poetry install --no-dev` - not recommended.

## Usage

### Jupyter notebooks
There are a collection of commonly used jupyter notebooks in the `notebooks/useful_notebooks` directory.  You can start a jupyter notebook server locally using `invoke notebook` from the top level directory.  This should launch the server and open a browser page where the notebooks can be accessed.

**IMPORTANT!** - You should create your own folder in the `notebooks` directory named `Yourname_scripts`.  This folder is where you should create, access and run your notebooks.  If you want to start with one of the notebooks in the useful_notebooks directory please create a copy and move it to your own folder.  This keeps the repository clean and organized.  Please **DO NOT** run notebooks in the useful_notebooks directory and commit the results to the repository.

### Scripts

The scripts directory contains some useful command line scripts.  They can be run from the top level directory using `python scripts/script_name --options`.  Using `--help` shows available options.  In general, modified versions and bespoke scripts should not be committed to the repository - or alternatively committed to a separate non-master branch.

As scripts are developed and refined `tool.poetry.scripts` directives can be added to facilitate script usage - see `pyproject.toml` file example.
