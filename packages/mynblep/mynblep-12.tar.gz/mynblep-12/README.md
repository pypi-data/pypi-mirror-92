# mynblep
MinBLEPs library including fast naive waveform conversion

## Install
These are generic installation instructions.

### To use, permanently
The quickest way to get started is to install the current release from PyPI:
```
pip3 install --user mynblep
```

### To use, temporarily
If you prefer to keep .local clean, install to a virtualenv:
```
python3 -m venv venvname
venvname/bin/pip install mynblep
. venvname/bin/activate
```

### To develop
First clone the repo using HTTP or SSH:
```
git clone https://github.com/combatopera/mynblep.git
git clone git@github.com:combatopera/mynblep.git
```
Now use pyven's pipify to create a setup.py, which pip can then use to install the project editably:
```
python3 -m venv pyvenvenv
pyvenvenv/bin/pip install pyven
pyvenvenv/bin/pipify mynblep

python3 -m venv venvname
venvname/bin/pip install -e mynblep
. venvname/bin/activate
```
