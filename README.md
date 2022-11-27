

## 0. Summary
- These scripts use [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/user-documentation.html)


## 1.  Environment Setup
### - Setup [Python Virtual Env (venv)](https://docs.python.org/3/library/venv.html)
Run: `python3 -m venv venv`
### - Install packages
```bash
source venv/bin/activate # This command is for linux
pip install -r requirements.txt
```
### - Make jupyter use venv
Run: 
```
python -m ipykernel install --user
ipython kernel install --user --name=venv
```

### - Modify Jupyter Notebook configurations (optional) 
Run: `jupyter notebook --generate-config`

Edit file `/home/${USER}/.jupyter/jupyter_notebook_config.py`

Find, uncomment and set `c.NotebookApp.open_browser` to `False`

### - Jupyter theme (optional)
```bash
jt -l
jt -t <theme-name>
```
and restart the jupyter if itis already started.

## 2. Start Jupyter
Run: `jupyter notebook --allow-root`

Go to the path displayed in the terminal.

To full flow, use file `tsaug-final.ipynb`

To explore data with few samples, use files `tsaug-*-experiment.ipynb`

When in the notebook, choose `Kernel` -> `Change kernel` -> `venv`

## 3. Data
Create a folder name `data`

Put data files in `data` 
