import argparse
import logging
import os
from collections import defaultdict

import numpy as np


def setup_parser(**kwargs) -> argparse.ArgumentParser:
    """
    Setup TALON argument parser.

    This function returns an argparse.ArgumentParser object with
    ``allow_abbrev=True`` and ``add_help=True``.

    Args:
        kwargs: dict
            dictionary that will be passed to the constructor of
            argparse.ArgumentParser.
    Return:
        argparse.ArgumentParser object with the passed options plus
        ``allow_abbrev=True`` and ``add_help=True``
    """
    kwargs['allow_abbrev'] = True
    kwargs['add_help'] = True

    parser = argparse.ArgumentParser(**kwargs)

    return parser


def add_ndir_to_input(parser: argparse.ArgumentParser):
    """
    This function adds the number of directions as input argument to a parser.

    The ``--ndir`` argument is added to ``parser``. The argument takes as input
    an integer which by default is equal to 1000.

    Args:
        parser: argparse.ArgumentParser
            Argument parser.
    """
    parser.add_argument(
        '--ndir',
        type=int,
        default=1000,
        metavar='number',
        help='Number of directions for the voxelization. Default: %(default)s.'
    )


def add_verbosity_and_force_to_parser(parser: argparse.ArgumentParser):
    """
    This function adds the verbosity and force parameters to a parser.

    After calling this method, the input parser will have the following boolean
    arguments.

    - ``--force``
    - ``--quiet``
    - ``--warn``
    - ``--info``
    - ``--debug``

    Args:
        parser: argparse.ArgumentParser
            Argument parser.
    """
    parser.add_argument(
        '--force',
        action='store_true',
        help="Overwrite existing files."
    )

    verb = parser.add_mutually_exclusive_group()
    verb.add_argument(
        '--quiet',
        action='store_true',
        help='Do not display messages.'
    )
    verb.add_argument(
        '--warn',
        action='store_true',
        help='Display warning messages.'
    )
    verb.add_argument(
        '--info',
        action='store_true',
        help='Display information messages.'
    )
    verb.add_argument(
        '--debug',
        action='store_true',
        help='Display debug messages.'
    )


def parse_verbosity(args: argparse.Namespace):
    """
    This function applies the wanted verbosity level in logging specified by the
    parsed arguments given in input.

    The default level is logging.WARNING.

    Args:
        args: argparse.Namespace
            Namespace parsed from inputs.
    """
    level = logging.WARNING
    if args.debug:
        level = logging.DEBUG
    if args.info:
        level = logging.INFO
    if args.warn:
        level = logging.WARN
    if args.quiet:
        level = logging.CRITICAL

    logging.getLogger().setLevel(level)


def check_can_write_file(fpath: str, force: bool = False):
    """
    Check if a file can be written.

    The function checks if the file already exists, the user has the permission
    to write it, overwriting can be forced and, if the file does not exist, if
    the parent directory exists and is writable.

    Args:
        fpath: str
            path of the file to be checked.
        force: bool
            True if the file can be overwritten, False otherwise.

    Raises:
        FileExistsError : if the file exists and can not be overwritten.
        PermissionError :  if the file esists and the user does not have the
            permission to write it.
        PermissionError : if the file does not exist, the parent directory
            exists and the user does not have the permission to write a file in
            it.
        FileNotFoundError : if file does not exist and the parent directory
            does not exist.
    """
    if os.path.exists(fpath) and os.path.isfile(fpath):
        if os.access(fpath, os.W_OK):
            if force:
                return
            else:
                raise FileExistsError(f'Specify `--force` to overwrite '
                                      f'{fpath}')
        else:
            # Tests for this case seem to be platform-dependent, hence have
            # been removed from the testing suite.
            raise PermissionError(f'User does not have permission to write '
                                  f'{fpath}')
    else:
        d = os.path.dirname(os.path.abspath(fpath))
        if os.path.exists(d):
            if os.access(d, os.W_OK):
                return
            else:
                raise PermissionError(f'User does not have permission to '
                                      f'write file in directory {d}')
        else:
            raise FileNotFoundError(f'Directory does not exist: {d}')


def assignment_to_mapping(fpath: str, undirected: bool = True) -> defaultdict:
    """
    This function creates a mapping object from a streamline assignment file.

    Args:
        fpath: str
            Path to the file whose rows contain the assignment of each
            streamline. E.g., if the n-th row is '5 17', the n-th streamline is
            assigned to regions 5 and 17. The region labels must be integer
            values and separated by a blank space. Lines starting with # are
            skipped.
        undirected: bool
            True if the mapping must be undirected, False otherwise.
    Returns:
        defaultdict
            Dictionary with keys being pairs of regions connected by
            streamlines and values being the list of streamline indices of
            those streamlines connecting the corresponding regions.
    """
    mapping = defaultdict(lambda: [])

    i = 0
    with open(fpath, 'r') as f:
        while True:
            line = f.readline()
            if len(line) == 0:
                break
            elif line[0] == '#':
                continue
            logging.debug(f'Streamline {i} connects {line.strip()}.')

            a, b = line.split(' ')
            coord = (int(a), int(b))
            if undirected:
                coord = tuple(sorted(coord))
            mapping[coord].append(i)
            i += 1
    return mapping


def mapping_to_groups_weights(mapping: defaultdict,
                              connectome: np.ndarray = None) -> (
        list, np.ndarray):
    """
    Extract the streamline groups and weights from a mapping object.

    Groups are lists of streamline indices that form a bundle.
    Weights are defined as follows: let :math:`N_g` be the number of
    streamlines in group :math:`g`, and let :math:`c_g` be the connectivity
    between the regions linked by streamline bundle :math:`g`.
    Each group :math:`g` is then associated to a weight equal to

        .. math::
            w_g = [N_g \cdot (1 + c_g)]^{-1}.

    Args:
        mapping: defaultdict
            dictionary with keys being pairs of regions connected by
            streamlines and values being the list of streamline indices of
            those streamlines connecting the corresponding regions.
        connectome: np.ndarray
            connectivity matrix to be employed. The first row and column
            correspond to the zero label.
    Returns:
        tuple of length 2
            - list of groups
            - 1-dimensional np.ndarray with one weight per group
    """
    groups = []
    weights = []
    if connectome is None:
        def c(*args):
            return 0.
    else:
        def c(i, j):
            return connectome[i, j]

    for key, value in mapping.items():
        groups.append(value)
        w = 1.0 / (np.sqrt(len(value)) * (1 + c(*key)))
        weights.append(w)

    weights = np.asarray(weights)
    return groups, weights
