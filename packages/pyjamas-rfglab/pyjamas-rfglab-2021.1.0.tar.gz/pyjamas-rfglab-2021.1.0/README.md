# PyJAMAS

[**Py**JAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) is **J**ust **A** **M**ore **A**wesome **S**iesta.

## Documentation
You can find the official [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) documentation [**here**](https://pyjamas.readthedocs.io). 

## Installing PyJAMAS
The easiest way to install [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) is using [PyPi](https://pypi.org/project/pyjamas-rfglab/). 

### A note on the *Python interpreter*
[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) requires that you have [Python](https://www.python.org/downloads/) installed.  

[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) has been extensively tested with [Python 3.6, 3.7 and 3.8](https://www.python.org/downloads/).

We use type annotations, which were introduced in Python 3.6, so [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) will not work with Python versions prior to 3.6.

For Linux users, we strongly suggest using the most recent version of Python 3.8, which solves incompatibilities with Theano, a machine learning package used in [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/).

[PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) does **NOT** work with Python 2. 

### MacOS and Linux
Open a terminal. If you had previously installed [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/), we recommend uninstalling the previous version:

To install [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/), type:  

```python
python3 -m pip install --no-cache-dir -U pyjamas-rfglab
```

To run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/), type:  

```python
pyjamas
```

at the user prompt.

If the executable fails to run, you can also try to execute [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) by opening a terminal and typing:

```python
python3 -m pyjamas.pjscore
```

Alternatively, if you clone this repository, you can run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) by opening a terminal and navigating to the folder that contains the code using the **cd** command. Once in the folder, type:

```python
python3 pjscore.py
```

### Windows
Before installing [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/), you will need to install  [Shapely](https://pypi.org/project/Shapely/), a package used in [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) to represent geometric objects such as points or polygons. Under Windows, [Shapely](https://pypi.org/project/Shapely/) fails to install with the [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) [PyPi](https://pypi.org/project/pyjamas-rfglab/) package. It is recommended to start by manually installing [Shapely](https://pypi.org/project/Shapely/). To that end, download the appropriate Shapely version from [this link](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely). For example, use  Shapely‑1.6.4.post2‑cp37‑cp37m‑win_amd64.whl for a 64-bit machine running Python 3.7. Open a command prompt and navigate to the folder that contains the downloaded .whl file using the **cd** command. Complete the installation of [Shapely](https://pypi.org/project/Shapely/) by typing:

```python
python -m pip install Shapely‑1.6.4.post2‑cp37‑cp37m‑win_amd64.whl
```
substituting the downloaded file name.


Once [Shapely](https://pypi.org/project/Shapely/), has been set up, you can proceed with a regular [PyPi](https://pypi.org/project/pyjamas-rfglab/) installation of [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/). Open a command prompt and type:  

```python
python -m pip install --no-cache-dir -U pyjamas-rfglab
```

To run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) type:  

```python
pyjamas
```

at the user prompt.  

If the executable fails to run, you can also try to execute [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) by opening a command prompt and typing:

```python
python -m pyjamas.pjscore
```

Alternatively, if you clone this repository, you can run [PyJAMAS](https://bitbucket.org/rfg_lab/pyjamas/src/master/) by opening a command prompt and navigating to the folder that contains the code using the **cd** command. Once in the folder, type:

```python
python pjscore.py
```