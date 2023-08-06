Welcome to talon's homepage!
=================================
[![pipeline status](https://gitlab.inria.fr/cobcom/talon/badges/master/pipeline.svg)](https://gitlab.inria.fr/cobcom/talon/-/commits/master) 
[![coverage report](https://gitlab.inria.fr/cobcom/talon/badges/master/coverage.svg)](https://gitlab.inria.fr/cobcom/talon/-/commits/master) 
[![Documentation Status](https://readthedocs.org/projects/cobcom-talon/badge/?version=latest)](https://cobcom-talon.readthedocs.io/en/latest/?badge=latest)
  
`talon` is a pure Python package that implements Tractograms As Linear
Operators in Neuroimaging.

The software provides the ``talon`` Python module, which includes all the
**functions and tools that are necessary for filtering a tractogram**.
In particular, specific functions are devoted to:

* Transforming a tractogram into a linear operator.
* Solving the inverse problem associated to the filtering of a tractogram.
* Use GPUs to speed up these operations.

The package is [available at Pypi](https://pypi.org/project/cobcom-talon/)
and can be easily installed from the command line.
```bash
    pip install cobcom-talon
```
Talon is a free software released under [MIT license](LICENSE) and the 
documentation is available on 
[Read the Docs](https://cobcom-talon.readthedocs.io/).


Getting help
------------
The preferred way to get assistance in running code that uses ``talon`` is
through the issue system of the
[Gitlab repository](https://gitlab.inria.fr/cobcom/talon) where the source
code is available.
Developers and maintainers frequently check newly opened issues and will be
happy to help you.


Contributing guidelines
-----------------------
The development happens in the ``devel`` branch of the
[Gitlab repository](https://gitlab.inria.fr/cobcom/talon) while the
``master`` is kept for the stable releases only.
We will consider only merge requests towards the ``devel`` branch.


How to cite
-----------
If you publish works using talon, please cite us as follows:

>Matteo Frigo, Mauro Zucchelli, Rachid Deriche, Samuel Deslauriers-Gauthier.
"TALON: Tractograms As Linear Operators in Neuroimaging." CoBCoM, 2021. 
https://hal.archives-ouvertes.fr/hal-03116143
