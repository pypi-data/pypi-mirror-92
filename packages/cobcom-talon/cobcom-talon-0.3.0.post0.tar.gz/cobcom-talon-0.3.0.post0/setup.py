# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md', 'r') as f:
    long_description = f.read()


# Read the version from the main package.
with open('talon/__init__.py') as f:
    for line in f:
        if '__version__' in line:
            _, version, _ = line.split("'")
            break


setup(
    author='Samuel Deslauriers-Gauthier, Matteo Frigo, Mauro Zucchelli',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],
    description='A Python package that implements Tractograms As Linear '
                'Operators in Neuroimaging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['nibabel', 'numpy', 'pyunlocbox', 'scipy'],
    extras_require={
        'opencl': ['pyopencl', 'pocl'],
    },
    name='cobcom-talon',
    packages=['talon', 'talon.cli'],
    python_requires='>=3',
    scripts=['script/talon'],
    url='https://gitlab.inria.fr/cobcom/talon',
    version=version,
    project_urls={
        'Source': 'https://gitlab.inria.fr/cobcom/talon',
        'Bug Reports': 'https://gitlab.inria.fr/cobcom/talon/issues',
        'Documentation': 'https://cobcom-talon.readthedocs.io',
    },
)
