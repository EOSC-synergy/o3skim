import unittest

from o3skim import utils


dict_1 = {'a': 1, 'c': 0, 'z': {'a': 1, 'c': 0}}
dict_2 = {'b': 2, 'c': 3, 'z': {'b': 2, 'c': 3}}


class Tests_mergedict(unittest.TestCase):

    def test_merge_d1d2(self):
        dict_3 = dict_1.copy()
        utils.mergedicts(dict_3, dict_2)
        self.assertEqual(dict_2, {'b': 2, 'c': 3, 'z': {'b': 2, 'c': 3}})
        self.assertEqual(dict_3['a'], 1)
        self.assertEqual(dict_3['b'], 2)
        self.assertEqual(dict_3['c'], 3)
        self.assertEqual(dict_3['z'], {'a': 1, 'b': 2, 'c': 3})

    def test_merge_d2d1(self):
        dict_3 = dict_2.copy()
        utils.mergedicts(dict_3, dict_1) 
        self.assertEqual(dict_1, {'a': 1, 'c': 0, 'z': {'a': 1, 'c': 0}})
        self.assertEqual(dict_3['a'], 1)
        self.assertEqual(dict_3['b'], 2)
        self.assertEqual(dict_3['c'], 0)
        self.assertEqual(dict_3['z'], {'a': 1, 'b': 2, 'c': 0})
