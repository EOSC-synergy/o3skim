import copy
import os
import tempfile
import unittest
import yaml

from o3skim import utils


dict_1 = {'a': 1, 'c': 0, 'z': {'a': 1, 'c': 0}}
dict_2 = {'b': 2, 'c': 3, 'z': {'b': 2, 'c': 3}}


class Tests_YAMLLoad(unittest.TestCase):

    def setUp(self) -> None:
        self.ymlfile = tempfile.NamedTemporaryFile(mode='w')
        yaml.dump(dict_1, self.ymlfile, allow_unicode=True)

    def tearDown(self) -> None:
        self.ymlfile.close()

    def test_correct_content(self):
        self.assertEqual(dict_1, utils.load(self.ymlfile.name))


class Tests_YAMLSave(unittest.TestCase):

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.prevdir = os.getcwd()
        os.chdir(self.tempdir.name)
        utils.save("metadata.yaml", metadata=dict_1)

    def tearDown(self) -> None:
        os.chdir(self.prevdir)
        self.tempdir.cleanup()


    def test_isfile(self):
        self.assertTrue(os.path.isfile("metadata.yaml"))

    def test_filecontent(self):
        with open("metadata.yaml", "r") as ymlfile:
            self.assertEqual(dict_1, yaml.safe_load(ymlfile))


class Tests_mergedict(unittest.TestCase):

    def test_merge_d1d2(self):
        dict_3 = copy.deepcopy(dict_1)
        utils.mergedicts(dict_3, dict_2)
        self.assertEqual(dict_2, {'b': 2, 'c': 3, 'z': {'b': 2, 'c': 3}})
        self.assertEqual(dict_3['a'], 1)
        self.assertEqual(dict_3['b'], 2)
        self.assertEqual(dict_3['c'], 3)
        self.assertEqual(dict_3['z'], {'a': 1, 'b': 2, 'c': 3})

    def test_merge_d2d1(self):
        dict_3 = copy.deepcopy(dict_2)
        utils.mergedicts(dict_3, dict_1)
        self.assertEqual(dict_1, {'a': 1, 'c': 0, 'z': {'a': 1, 'c': 0}})
        self.assertEqual(dict_3['a'], 1)
        self.assertEqual(dict_3['b'], 2)
        self.assertEqual(dict_3['c'], 0)
        self.assertEqual(dict_3['z'], {'a': 1, 'b': 2, 'c': 0})

    def test_merge_with_exception(self):
        def raise_exception(x, y): raise Exception(x, y)
        with self.assertRaises(Exception) as cm:
            utils.mergedicts({'a': 1}, {'a': 2}, raise_exception)
        self.assertEqual(cm.exception.args, (1, 2))
