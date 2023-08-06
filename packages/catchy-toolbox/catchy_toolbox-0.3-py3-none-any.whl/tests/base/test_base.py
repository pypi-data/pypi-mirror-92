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

import unittest

import catchy
from catchy.base.roughness import _next_power_of_2
from tests.common import DEFAULT_SAMPLE_RATE
from tests.common import get_test_audio_file_path


class Roughness(unittest.TestCase):
    def test_next_power_of_2(self):
        self.assertEqual(_next_power_of_2(2), 2)
        self.assertEqual(_next_power_of_2(3), 4)
        self.assertEqual(_next_power_of_2(6), 8)
        self.assertEqual(_next_power_of_2(8), 8)
        self.assertEqual(_next_power_of_2(1027), 2048)


class HPCP(unittest.TestCase):
    def test_hpcp(self):
        file = get_test_audio_file_path()
        audio = catchy.mono_load(file, DEFAULT_SAMPLE_RATE)
        t, hpcp = catchy.hpcp(audio, DEFAULT_SAMPLE_RATE)

        self.assertTrue(len(t) > 0)
        self.assertTrue(len(hpcp) > 0)
        self.assertEqual(len(t), len(hpcp))


if __name__ == '__main__':
    unittest.main()
