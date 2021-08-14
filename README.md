## Time-Weighted Average Market Maker (TWAMM) Reference Implementation

See [twamm_demo.ipynb](twamm_demo.ipynb) for usage.

Test with nosetests.

### install

``` bash
# create virtualenv
python3 -m venv twamm-venv
source twamm-venv/bin/activate

# install dependencies
pip install -r requirements.txt
# register virtualenv to jupyter kernal
python -m ipykernel install --name=twamm
```

### start

``` bash
jupyter-lab
```
