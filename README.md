# Jupyter Project Template

This repository contains scripts and utilities for managing Jupyter notebooks in a Git repository. <br>
Because of Jupyter's JSON format, version control can be difficult. <br>
This template aims to address this issue as well as add additional functionality for Quarto rendering.

This is done using the `jupytext` package to convert between `.py` and `.ipynb` files, with Git only tracking the former. <br>
The provided scripts allow for an easy workflow to convert between these formats and avoid Jupyter's version control issues.

## Project Structure
- `src/`: Python source files tracked by Git
- `notebooks/`: Jupyter notebook files stored locally
- `html/`: Rendered Quarto HTML output
- `scripts/`: Utility scripts

## Installation
1. Clone or download this repository into a new Git repository
2. Ensure Python 3.x is installed
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Jupyter Notebook Synchronization
`scripts/jupyter_sync.py` keeps `.py` and `.ipynb` files synchronized.
This allows us to avoid the issues of version control with Jupyter notebooks.

```bash
python scripts/jupyter_sync.py
```
- Converts between .py and .ipynb files
- Adds new files to Git tracking

## Quarto Rendering Scripts

### Single Notebook Rendering
Render and open a single notebook:
```bash
python scripts/render_quarto_single.py notebooks/your_notebook.ipynb
```

### Batch Notebook Rendering
Render all notebooks in the `notebooks/` directory:
```bash
python scripts/render_quarto_all.py
```

## Requirements
- Python 3.x
- Jupytext
- Quarto
- Git