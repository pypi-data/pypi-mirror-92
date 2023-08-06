# Py-GSuite-APIs

This package is meant to standardize and simplify working with Google Sheets, Slides, and Drive APIs through utility classes and functions. It also seeks to provide an interactive environment to inspect and valdiate the shape/structure of requests by using Pydantic models that mirror the Classes implemented by Google APIs.

## Development

Create a new conda environment:

```bash
conda env create -f environment.yml && conda activate pyGsuiteApis
```

And install the appropriate packages:

```bash
python setup.py develop
```

