# 
# MIT License
# 
# Copyright (c) 2020 Music Cognition Group, University of Amsterdam
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os.path
import shutil
import tempfile
import unittest

import catchy
from tests.common import DEFAULT_SAMPLE_RATE
from tests.common import get_test_dir


class BaseFeaturesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_hpcp(self):
        data_dir = get_test_dir()
        catchy.process_base_features(data_dir, self.test_dir, DEFAULT_SAMPLE_RATE, features=['hpcp'])

        file_path = os.path.join(self.test_dir, 'hpcp', 'test.csv')
        self.assertTrue(os.path.exists(file_path))

        feature = catchy.read_feature(file_path)
        t_size, n_chroma = feature.shape
        self.assertEqual(n_chroma, 12 + 1)
        self.assertTrue(t_size > 0)

    def test_melodia(self):
        data_dir = get_test_dir()
        catchy.process_base_features(data_dir, self.test_dir, DEFAULT_SAMPLE_RATE, features=['melodia'])

        file_path = os.path.join(self.test_dir, 'melodia', 'test.csv')
        self.assertTrue(os.path.exists(file_path))

        feature = catchy.read_feature(file_path)
        t_size, d = feature.shape
        self.assertEqual(d, 2)
        self.assertTrue(t_size > 0)


if __name__ == '__main__':
    unittest.main()
