# spike-recorder

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![Gitter][gitter-badge]][gitter-link]

This package implements a Python interface for the 
[Backyard Brains Spike Recorder](https://backyardbrains.com/products/spikerecorder), a neural recording application. It
is based off a [fork](https://github.com/davidt0x/Spike-Recorder) of the original C++ code, found 
[here](https://github.com/BackyardBrains/Spike-Recorder). In addition, it contains two psychological experiment 
applications written in Python that control and record events via the SpikeRecorder. 

## Installation

You can install this library from [PyPI](https://pypi.org/project/spike-recorder/) with pip:

```bash
python -m pip install spike-recorder
```

## Usage

To run the SpikeRecorder application simply invoke it on the command line

```bash
spike-recorder
```

To launch the Iowa Gambling Task Experiment, run:

```bash
iowa
```

To launch the Libet Task Experiment, run:

```bash
libet
```





[actions-badge]:            https://github.com/davidt0x/py-spike-recorder/workflows/CI/badge.svg
[actions-link]:             https://github.com/davidt0x/py-spike-recorderactions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/spike-recorder
[conda-link]:               https://github.com/conda-forge/spike-recorder-feedstock
[gitter-badge]:             https://badges.gitter.im/PrincetonUniversity/py-spike-recorder.svg
[gitter-link]:              https://gitter.im/PrincetonUniversity/py-spike-recorder?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
[pypi-link]:                https://pypi.org/project/spike-recorder/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/spike-recorder
[pypi-version]:             https://badge.fury.io/py/spike-recorder.svg
[rtd-badge]:                https://readthedocs.org/projects/spike-recorder/badge/?version=latest
[rtd-link]:                 https://spike-recorder.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
