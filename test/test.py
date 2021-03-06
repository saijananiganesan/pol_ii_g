#!/usr/bin/env python

import unittest
import os
import shutil
import sys
import subprocess
import ihm.reader

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))

class Tests(unittest.TestCase):
    def test_simple(self):
        """Test model building"""
        os.chdir(os.path.join(TOPDIR, 'production_scripts'))
        p = subprocess.check_call(["python", "sample.py", "--test"])
        # todo: assert outputs, run analysis

    def test_mmcif(self):
        """Test generation of mmCIF output"""
        os.chdir(os.path.join(TOPDIR, 'production_scripts'))
        if os.path.exists("pol_ii_g.cif"):
            os.unlink("pol_ii_g.cif")
        # Potentially override methods that need network access
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.join(TOPDIR, 'test', 'mock') \
                            + ':' + env.get('PYTHONPATH', '')
        p = subprocess.check_call(
                ["python", "sample.py", "--mmcif", "--dry-run"], env=env)
        # Check output file
        self._check_mmcif_file('pol_ii_g.cif')

    def _check_mmcif_file(self, fname):
        with open(fname) as fh:
            s, = ihm.reader.read(fh)
        self.assertEqual(len(s.citations), 1)
        self.assertEqual(s.citations[0].doi, '10.1038/s41594-018-0118-5')
        self.assertEqual(len(s.software), 2)
        self.assertEqual(len(s.orphan_starting_models), 12)
        # Should be 1 state
        self.assertEqual(len(s.state_groups), 1)
        state1, = s.state_groups[0]
        # Should be 1 model
        self.assertEqual(sum(len(x) for x in state1), 1)
        # Check # of spheres and atoms in each model
        m = state1[0][0]
        self.assertEqual(len(m._spheres), 3640)
        self.assertEqual(len(m._atoms), 0)
        # Should be 1 ensemble
        self.assertEqual([e.num_models for e in s.ensembles], [100])
        # Just one restraint - crosslinks
        xl, = s.restraints
        self.assertEqual(len(xl.experimental_cross_links), 40)
        self.assertEqual(len(xl.cross_links), 40)


if __name__ == '__main__':
    unittest.main()
