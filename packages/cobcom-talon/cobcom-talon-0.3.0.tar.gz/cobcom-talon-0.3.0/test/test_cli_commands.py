import argparse
import importlib.util
import pickle
import tempfile
from unittest import TestCase

import nibabel as nib
import numpy as np
import scipy.sparse as sp

import talon
import talon.cli
from talon.cli import commands


def get_example_streamlines():
    i = np.array([[0, 0, 0], [10, 10, 10]], dtype=np.float)
    j = np.array([[10, 0, 0], [0, 10, 10]], dtype=np.float)
    k = np.array([[10, 10, 0], [0, 0, 10]], dtype=np.float)
    s = [i, j, k]

    return s


class TestVoxelize(TestCase):
    def test_setup_parser(self):
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        commands.voxelize.add_parser(subparsers)
        self.assertTrue(subparsers.choices.get('voxelize') is not None)
        self.assertIsInstance(subparsers.choices.get('voxelize'),
                              argparse.ArgumentParser)

    def test_execution(self):
        streamlines = get_example_streamlines()
        ftck = tempfile.NamedTemporaryFile(suffix='.tck')
        tractogram = nib.streamlines.Tractogram(streamlines,
                                                affine_to_rasmm=np.eye(4))
        nib.streamlines.save(tractogram, ftck.name)

        vol = nib.Nifti1Image(np.zeros((11, 11, 11)), affine=np.eye(4))
        fvol = tempfile.NamedTemporaryFile(suffix='.nii.gz')
        nib.save(vol, fvol.name)

        fidx = tempfile.NamedTemporaryFile(suffix='.npz')
        fwei = tempfile.NamedTemporaryFile(suffix='.npz')

        args = ftck.name, fvol.name, fidx.name, fwei.name
        commands.voxelize.run(*args, force=True, ndir=1000)

        idx = sp.load_npz(fidx.name)
        wei = sp.load_npz(fwei.name)

        dirs1000 = talon.utils.directions(1000)
        gt_idx, gt_wei = talon.voxelize(streamlines, dirs1000, vol.shape)

        # compare result of script with result of talon.voxelize
        np.testing.assert_equal(idx.row, gt_idx.row)
        np.testing.assert_equal(idx.col, gt_idx.col)
        np.testing.assert_equal(idx.data, gt_idx.data)
        np.testing.assert_equal(wei.row, gt_wei.row)
        np.testing.assert_equal(wei.col, gt_wei.col)
        np.testing.assert_almost_equal(wei.data, gt_wei.data)

        for f in [ftck, fvol, fidx, fwei]:
            f.close()


class TestFilter(TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        # setup
        self.streamlines = get_example_streamlines()
        self.shape = (11, 11, 11)

        self.ftck = tempfile.NamedTemporaryFile(suffix='.tck')
        tractogram = nib.streamlines.Tractogram(self.streamlines,
                                                affine_to_rasmm=np.eye(4))
        nib.streamlines.save(tractogram, self.ftck.name)

        self.dirs1000 = talon.utils.directions(1000)

        i, w = talon.voxelize(self.streamlines, self.dirs1000, self.shape)
        g = np.zeros((1000, 1))
        g[:, 0] = 1.

        # linear operator
        self.linear_operator = talon.operator(g, i, w)

        # reference data
        self.gt_x = np.array([0., 1., 2.])
        self.gt_y = self.linear_operator @ self.gt_x

        self.fdata = tempfile.NamedTemporaryFile(suffix='.nii.gz')
        vol = nib.Nifti1Image(self.gt_y.reshape(self.shape), affine=np.eye(4))
        nib.save(vol, self.fdata.name)

    def test_setup_parser(self):
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        commands.filter.add_parser(subparsers)
        self.assertTrue(subparsers.choices.get('filter') is not None)
        self.assertIsInstance(subparsers.choices.get('filter'),
                              argparse.ArgumentParser)

    def test_execution_default(self):
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        args = parser.parse_args(
            [self.ftck.name, self.fdata.name, out_weights.name, '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        commands.filter.run(**parameters)

        # compare against talon.solve
        sol = talon.solve(self.linear_operator, self.gt_y,
                          reg_term=talon.regularization(non_negativity=True),
                          verbose='NONE')
        x = np.loadtxt(out_weights.name)
        np.testing.assert_almost_equal(x, sol.x, 3)

        out_weights.close()

    def test_execution_fit(self):
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        # create group structure
        fassign = tempfile.NamedTemporaryFile(suffix='.txt')
        with open(fassign.name, 'w') as f:
            f.writelines(['1 2\n', '3 1\n', '1 3\n'])
        mapping = talon.cli.utils.assignment_to_mapping(fassign.name)

        fconn = tempfile.NamedTemporaryFile(suffix='.txt')
        connectome = np.zeros((4, 4))
        connectome[1, 2] = 0.3
        connectome[2, 1] = 0.3
        connectome[1, 3] = 0.7
        np.savetxt(fconn.name, connectome)

        groups, weights = talon.cli.utils.mapping_to_groups_weights(mapping,
                                                                    connectome)

        sigma = 1e-4
        llambda = np.linalg.norm(self.linear_operator.T @ self.gt_y, 2)
        llambda *= np.max(1 / weights)
        llambda *= sigma

        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        args = parser.parse_args(
            [self.ftck.name, self.fdata.name, out_weights.name,
             '--connectome', fconn.name,
             '--streamline-assignment', fassign.name,
             '--sigma', str(sigma),
             '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        commands.filter.run(**parameters)

        # compare against talon.solve
        regterm = talon.regularization(non_negativity=True, groups=groups,
                                       weights=weights,
                                       regularization_parameter=1e-4)
        sol = talon.solve(self.linear_operator, self.gt_y, reg_term=regterm,
                          verbose='NONE')
        x = np.loadtxt(out_weights.name)
        np.testing.assert_almost_equal(x, sol.x, 3)

        fassign.close()
        fconn.close()
        out_weights.close()

    def test_in_precomputed_giw(self):
        # fg = tempfile.NamedTemporaryFile(suffix='.npy')
        # g = self.linear_operator.generators
        # np.save(fg.name, g)

        # indices
        fi = tempfile.NamedTemporaryFile(suffix='.npz')
        i = self.linear_operator._indices_of_generators
        sp.save_npz(fi.name, i)

        # weights
        fw = tempfile.NamedTemporaryFile(suffix='.npz')
        w = self.linear_operator._weights
        sp.save_npz(fw.name, w)

        # parse arguments
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        fassign = tempfile.NamedTemporaryFile(suffix='.txt')
        with open(fassign.name, 'w') as f:
            f.writelines(['1 2\n', '3 1\n', '1 3\n'])
        mapping = talon.cli.utils.assignment_to_mapping(fassign.name)

        fconn = tempfile.NamedTemporaryFile(suffix='.txt')
        connectome = np.zeros((4, 4))
        connectome[1, 2] = 0.3
        connectome[2, 1] = 0.3
        connectome[1, 3] = 0.7
        np.savetxt(fconn.name, connectome)

        groups, weights = talon.cli.utils.mapping_to_groups_weights(mapping,
                                                                    connectome)

        sigma = 1e-4
        llambda = np.linalg.norm(self.linear_operator.T @ self.gt_y, 2)
        llambda *= np.max(1 / weights)
        llambda *= sigma

        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        args = parser.parse_args(
            [self.ftck.name, self.fdata.name, out_weights.name,
             '--connectome', fconn.name,
             '--streamline-assignment', fassign.name,
             '--sigma', str(sigma),
             '--precomputed-indices-weights', fi.name, fw.name,
             '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        commands.filter.run(**parameters)

        # compare against talon.solve
        regterm = talon.regularization(non_negativity=True, groups=groups,
                                       weights=weights,
                                       regularization_parameter=1e-4)
        sol = talon.solve(self.linear_operator, self.gt_y, reg_term=regterm,
                          verbose='NONE')
        x = np.loadtxt(out_weights.name)
        np.testing.assert_almost_equal(x, sol.x, 3)

        fassign.close()
        # fg.close()
        fi.close()
        fw.close()

    def test_out_linear_operator_giw(self):
        # parse arguments
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        fassign = tempfile.NamedTemporaryFile(suffix='.txt')
        with open(fassign.name, 'w') as f:
            f.writelines(['1 2\n', '3 1\n', '1 3\n'])
        mapping = talon.cli.utils.assignment_to_mapping(fassign.name)

        fconn = tempfile.NamedTemporaryFile(suffix='.txt')
        connectome = np.zeros((4, 4))
        connectome[1, 2] = 0.3
        connectome[2, 1] = 0.3
        connectome[1, 3] = 0.7
        np.savetxt(fconn.name, connectome)

        groups, weights = talon.cli.utils.mapping_to_groups_weights(mapping,
                                                                    connectome)

        sigma = 1e-4
        llambda = np.linalg.norm(self.linear_operator.T @ self.gt_y, 2)
        llambda *= np.max(1 / weights)
        llambda *= sigma

        out_g = tempfile.NamedTemporaryFile(suffix='.npy')
        out_i = tempfile.NamedTemporaryFile(suffix='.npz')
        out_w = tempfile.NamedTemporaryFile(suffix='.npz')
        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        args = parser.parse_args(
            [self.ftck.name, self.fdata.name, out_weights.name,
             '--connectome', fconn.name,
             '--streamline-assignment', fassign.name,
             '--sigma', str(sigma),
             '--save-generators-indices-weights',
             out_g.name, out_i.name, out_w.name,
             '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        commands.filter.run(**parameters)

        # compare against ground truth
        g = np.load(out_g.name)
        i = sp.load_npz(out_i.name)
        w = sp.load_npz(out_w.name)

        op = talon.operator(g, i, w).todense()
        gt = self.linear_operator.todense()
        np.testing.assert_almost_equal(op, gt)

        fassign.close()
        out_g.close()
        out_i.close()
        out_w.close()

    def test_out_linear_operator_pickle(self):
        # parse arguments
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        fassign = tempfile.NamedTemporaryFile(suffix='.txt')
        with open(fassign.name, 'w') as f:
            f.writelines(['1 2\n', '3 1\n', '1 3\n'])
        mapping = talon.cli.utils.assignment_to_mapping(fassign.name)

        fconn = tempfile.NamedTemporaryFile(suffix='.txt')
        connectome = np.zeros((4, 4))
        connectome[1, 2] = 0.3
        connectome[2, 1] = 0.3
        connectome[1, 3] = 0.7
        np.savetxt(fconn.name, connectome)

        groups, weights = talon.cli.utils.mapping_to_groups_weights(mapping,
                                                                    connectome)

        sigma = 1e-4
        llambda = np.linalg.norm(self.linear_operator.T @ self.gt_y, 2)
        llambda *= np.max(1 / weights)
        llambda *= sigma

        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        out_pickle = tempfile.NamedTemporaryFile(suffix='.pickle')
        args = parser.parse_args(
            [self.ftck.name, self.fdata.name, out_weights.name,
             '--connectome', fconn.name,
             '--streamline-assignment', fassign.name,
             '--sigma', str(sigma),
             '--save-operator-pickle', out_pickle.name,
             '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        commands.filter.run(**parameters)

        # compare against ground truth
        with open(out_pickle.name, 'rb') as f:
            lop = pickle.load(f)

        np.testing.assert_almost_equal(lop.todense(),
                                       self.linear_operator.todense())

        fassign.close()
        out_pickle.close()

    def test_opencl_operator_type(self):
        if importlib.util.find_spec('pyopencl') is not None:
            p = argparse.ArgumentParser()
            subparsers = p.add_subparsers()
            subparsers.required = True
            subparsers.dest = 'subcommand'
            parser = commands.filter.add_parser(subparsers)

            out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
            args = parser.parse_args(
                [self.ftck.name, self.fdata.name, out_weights.name,
                 '--operator-type', 'opencl',
                 '--force'])
            parameters = {k: v for k, v in vars(args).items() if k != 'func'}
            commands.filter.run(**parameters)

            # compare against talon.solve
            sol = talon.solve(self.linear_operator, self.gt_y,
                              reg_term=talon.regularization(
                                  non_negativity=True),
                              verbose='NONE')
            x = np.loadtxt(out_weights.name)
            np.testing.assert_almost_equal(x, sol.x, 3)

            out_weights.close()

    def test_save_opencl(self):
        if importlib.util.find_spec('pyopencl') is not None:
            p = argparse.ArgumentParser()
            subparsers = p.add_subparsers()
            subparsers.required = True
            subparsers.dest = 'subcommand'
            parser = commands.filter.add_parser(subparsers)

            out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
            out_pickle = tempfile.NamedTemporaryFile(suffix='.pickle')
            args = parser.parse_args(
                [self.ftck.name, self.fdata.name, out_weights.name,
                 '--operator-type', 'opencl',
                 '--save-operator-pickle', out_pickle.name,
                 '--force'])
            parameters = {k: v for k, v in vars(args).items() if k != 'func'}
            with self.assertRaises(ValueError):
                commands.filter.run(**parameters)

    def test_data_shape(self):
        p = argparse.ArgumentParser()
        subparsers = p.add_subparsers()
        subparsers.required = True
        subparsers.dest = 'subcommand'
        parser = commands.filter.add_parser(subparsers)

        out_weights = tempfile.NamedTemporaryFile(suffix='.txt')
        fdata_wrong_shape = tempfile.NamedTemporaryFile(suffix='.nii.gz')
        wrong_shape = list(self.shape) + [2]

        vol = np.random.rand(np.prod(wrong_shape)).reshape(wrong_shape)
        vol = nib.Nifti1Image(vol, affine=np.eye(4))
        nib.save(vol, fdata_wrong_shape.name)

        args = parser.parse_args(
            [self.ftck.name, fdata_wrong_shape.name, out_weights.name,
             '--force'])
        parameters = {k: v for k, v in vars(args).items() if k != 'func'}
        with self.assertRaises(ValueError):
            commands.filter.run(**parameters)

        out_weights.close()
        fdata_wrong_shape.close()
