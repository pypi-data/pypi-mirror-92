import unittest
import pandas as pd
from pathlib import Path
from pyhard.measures import Measures

_my_path = Path(__file__).parent


def load_data(name):
    path = _my_path.parents[1] / f'data/{name}/data.csv'
    df = pd.read_csv(path)
    df.index.name = 'Instances'
    return df


class TestMeasures(unittest.TestCase):
    test_data = ['iris', '2normals', 'overlap', 'easy', 'mix']

    def test_kdn(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.k_disagreeing_neighbors()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_ds(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.disjunct_size()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_dcp(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.disjunct_class_percentage()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_tdu(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.tree_depth_unpruned()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_tdp(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.tree_depth_pruned()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_cl(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.class_likeliood()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_cld(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.class_likeliood_diff()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_mv(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.minority_value()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_cb(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.class_balance()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_n1(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.borderline_points()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_n2(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.intra_extra_ratio()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_lsc(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.local_set_cardinality()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_lsr(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.ls_radius()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_harmfulness(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.harmfulness()
            self.assertTrue((result >= 0).all() and (result <= 1).all())

    def test_usefulness(self):
        for name in self.test_data:
            df = load_data(name)
            m = Measures(df)
            result = m.usefulness()
            self.assertTrue((result >= 0).all() and (result <= 1).all())
