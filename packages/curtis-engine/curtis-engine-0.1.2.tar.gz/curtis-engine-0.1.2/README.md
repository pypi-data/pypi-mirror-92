# Curtis: The Cardiovascular Unified Real-Time Intelligent System

![Python package](https://github.com/gantoreno/curtis-engine/workflows/Python%20package/badge.svg) ![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue) ![Upload Python Package](https://github.com/gantoreno/curtis-engine/workflows/Upload%20Python%20Package/badge.svg)

Curtis is a system whose purpose is to analyze cardiovascular health of a given person, this is done through ECG analysis (an existent ECG measuring system is needed to obtain the required values).

## How does it work?

Curtis acts as an expert system, a rule-based program that emulates a real-life expert way of thinking about a certain topic, those rules were obtained for Curtis using the "decision tree approach", in which some existent data was given to a decision tree classifier, and it categorized the data into branches of rules and decisions.

## Usage

First, install the `curtis-engine` package:

```sh
$ pip install curtis-engine
```

To start using Curtis, the `CurtisEngine` class must be imported, as well as `CurtisFact` for the fact declaration:

```python
>>> from curtis import CurtisEngine, CurtisFact
>>> curtis = CurtisEngine()
```

After that, use `curtis.declare_fact` method to declare a new `CurtisFact` object, which should contain all the ECG values needed for a diagnosis to be performed:

```python
>>> curtis.declare_fact(
...    CurtisFact(
...         sex=1,
...         age=89,
...         height=140,
...         weight=30,
...         HR=56,
...         Pd=122,
...         PQ=164,
...         QRS=118,
...         QT=460,
...         QTcFra=451
...     )
... )
```

Finally, to get a diagnosis over the declared fact, use the `curtis.diagnose` method:

```python
>>> diagnosis = curtis.diagnose()
>>> print(diagnosis)
60
```

The `curtis.diagnose` method returns a number (as seen). This number is a _diagnosis index_, which means it's a unique index for a given diagnosis. To see which diagnosis belongs to that index, import the `diagnosis_indexes` dictionary from the `curtis.utils.encoding` package, and use the diagnosis as the index:

```python
>>> from curtis.utils.encoding import diagnosis_indexes
>>> print(diagnosis_indexes[diagnostic])
Unifocal premature ventricular complexes
```

And voilà! you've made your first Curtis diagnosis. 🎉

## Docs

To see the docs, you can clone the repo and open the `docs` folder to serve it as a website.

Using [`serve`](https://www.npmjs.com/package/serve):

```sh
$ git clone github.com/gantoreno/curtis-engine.git
$ cd curtis-engine
$ serve docs
```

The documentation should now be available at [http://localhost:5000](http://localhost:5000).

## License

This project is licensed under the [Python Packaging Authority](https://www.pypa.io/en/latest/) license.
