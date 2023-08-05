import argparse
import logging
import os
import tempfile
from unittest import TestCase

import numpy as np

import talon.cli as cli


class TestUtils(TestCase):
    def test_setup_parser(self):
        p = cli.utils.setup_parser()

        self.assertIsInstance(p, argparse.ArgumentParser)
        self.assertTrue(p.allow_abbrev)
        self.assertTrue(p.add_help)

    def test_ndir_input(self):
        p = cli.utils.setup_parser()
        cli.utils.add_ndir_to_input(p)
        parsed_args = p.parse_known_args()[0]

        self.assertEqual(parsed_args.ndir, 1000)

    def test_add_verbose_and_force(self):
        p = cli.utils.setup_parser()
        cli.utils.add_verbosity_and_force_to_parser(p)

        parsed_args = p.parse_known_args()[0]
        self.assertEqual(parsed_args.force, False)
        self.assertEqual(parsed_args.debug, False)
        self.assertEqual(parsed_args.info, False)
        self.assertEqual(parsed_args.quiet, False)
        self.assertEqual(parsed_args.warn, False)

    def test_parse_verbosity_and_force(self):
        p = cli.utils.setup_parser()
        cli.utils.add_verbosity_and_force_to_parser(p)

        parsed_args = p.parse_args(['--force'])
        self.assertTrue(parsed_args.force)

        old_level = logging.getLogger().level
        parsed_args = p.parse_known_args()[0]
        cli.utils.parse_verbosity(parsed_args)
        self.assertEqual(logging.getLogger().level, logging.WARNING)

        parsed_args = p.parse_args(['--debug'])
        cli.utils.parse_verbosity(parsed_args)
        self.assertTrue(parsed_args.debug)
        self.assertEqual(logging.getLogger().level, logging.DEBUG)

        parsed_args = p.parse_args(['--info'])
        cli.utils.parse_verbosity(parsed_args)
        self.assertTrue(parsed_args.info)
        self.assertEqual(logging.getLogger().level, logging.INFO)

        parsed_args = p.parse_args(['--warn'])
        cli.utils.parse_verbosity(parsed_args)
        self.assertTrue(parsed_args.warn)
        self.assertEqual(logging.getLogger().level, logging.WARNING)

        parsed_args = p.parse_args(['--quiet'])
        cli.utils.parse_verbosity(parsed_args)
        self.assertTrue(parsed_args.quiet)
        self.assertEqual(logging.getLogger().level, logging.CRITICAL)

        logging.getLogger().setLevel(old_level)

    def test_check_can_write_file(self):
        # file exists AND file does not have write permission
        # with tempfile.NamedTemporaryFile() as tf:
        #     os.chmod(tf.name, 0o444)  # read only
        #     with self.assertRaises(PermissionError):
        #         cli.utils.check_can_write_file(fpath=tf.name)

        # file exists AND file has write permission AND no force
        with tempfile.NamedTemporaryFile() as tf:
            os.chmod(tf.name, 0o777)  # can write
            with self.assertRaises(FileExistsError):
                cli.utils.check_can_write_file(fpath=tf.name, force=False)

        # file exists AND file has write permission AND force
        with tempfile.NamedTemporaryFile() as tf:
            os.chmod(tf.name, 0o777)  # can write
            r = cli.utils.check_can_write_file(fpath=tf.name, force=True)
            self.assertTrue(r is None)

        # file does not exist AND directory does not exist
        with tempfile.TemporaryDirectory() as td:
            f = os.path.join(td, 'x', 'y')
            with self.assertRaises(FileNotFoundError):
                cli.utils.check_can_write_file(fpath=f)

        # file does not exist AND directory exists AND directory does not have
        # writing permission
        # with tempfile.TemporaryDirectory() as td:
            # os.chmod(td, 0o444)
            # f = os.path.join(td, 'x')
            # with self.assertRaises(PermissionError):
            #     cli.utils.check_can_write_file(fpath=f)

        # file does not exist AND directory exists AND directory has writing
        # permission
        with tempfile.TemporaryDirectory() as td:
            os.chmod(td, 0o777)
            f = os.path.join(td, 'x')
            r = cli.utils.check_can_write_file(fpath=f)
            self.assertTrue(r is None)

    def test_assignment_to_mapping(self):
        with tempfile.NamedTemporaryFile() as t:
            with open(t.name, 'w') as f:
                f.writelines(['# skip this text\n', '1 2\n', '2 1\n', '1 3\n',
                              '1 3\n'])
            mapping_undir = cli.utils.assignment_to_mapping(t.name)
            mapping_dir = cli.utils.assignment_to_mapping(t.name, False)

        self.assertTupleEqual(tuple(mapping_undir[(1, 2)]), (0, 1))
        self.assertTupleEqual(tuple(mapping_undir[(1, 3)]), (2, 3))
        self.assertEqual(len(mapping_undir.keys()), 2)

        self.assertTupleEqual(tuple(mapping_dir[(1, 2)]), (0,))
        self.assertTupleEqual(tuple(mapping_dir[(2, 1)]), (1,))
        self.assertTupleEqual(tuple(mapping_dir[(1, 3)]), (2, 3))
        self.assertEqual(len(mapping_dir.keys()), 3)

    def test_mapping_to_groups_weights(self):
        with tempfile.NamedTemporaryFile() as t:
            with open(t.name, 'w') as f:
                f.writelines(['1 2\n', '2 1\n', '1 3\n', '1 3\n'])
            mapping = cli.utils.assignment_to_mapping(t.name)

        # without connectome
        g, w = cli.utils.mapping_to_groups_weights(mapping)
        self.assertTrue([0, 1] in g)
        self.assertTrue([2, 3] in g)
        self.assertListEqual([[0, 1], [2, 3]], g)
        gt = np.asarray([1 / np.sqrt(2), ] * 2)
        np.testing.assert_almost_equal(w, gt)

        # with connectome
        connectome = np.zeros((4, 4))
        connectome[1, 2] = 0.5
        connectome[2, 1] = 0.5
        connectome[1, 3] = 0.7
        connectome[3, 1] = 0.7
        g, w = cli.utils.mapping_to_groups_weights(mapping, connectome)

        gt = np.asarray([1 / np.sqrt(2), ] * 2)
        gt *= 1 / (1 + np.asarray([0.5, 0.7]))
        np.testing.assert_almost_equal(w, gt)
