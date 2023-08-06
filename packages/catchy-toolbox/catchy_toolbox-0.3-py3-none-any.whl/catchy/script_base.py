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

import os
from catchy import base
from catchy.io import mono_load
from catchy.utils import write_feature

EXTENSIONS = ["wav", "mp3"]


def process_base_features(input_dir, output_dir, sample_rate=22050, features=None):
    features_gen = base_features_in_dir_generator(input_dir, sample_rate=sample_rate, features=features)
    for file, feature_map in features_gen:
        filename = os.path.split(file)[-1]
        for feature_name, feature in feature_map.items():
            write_feature(list(feature), [output_dir, feature_name, filename.split('.')[-2]])


def base_features_in_dir_generator(directory, sample_rate=22050, features=None):
    files = _get_files_from_directory(directory, EXTENSIONS)
    return base_features_generator(files, sample_rate, features)


def base_features_generator(list_files, sample_rate=22050, features=None):
    if features is None:
        return ((file, _file_compute_all_base_features(file, sample_rate)) for file in list_files)

    return ((file, _file_compute_base_features(file, sample_rate, features)) for file in list_files)


def _get_files_from_directory(directory, extensions):
    files = []
    for filename in os.listdir(directory):
        if filename.split('.')[-1] in extensions:
            files.append(os.path.join(directory, filename))
    return files


def _file_compute_base_features(file, sample_rate, features):
    feature_function_map = {
        'mfcc': base.get_mfcc,
        'hpcp': base.hpcp,
        'melodia': base.melodia,
        'beats': base.get_beats,
        'onsets': base.get_onsets,
        'roughness': base.roughness,
        'loudness': base.loudness,
        'sharpness': base.sharpness
    }

    feature_map = {}
    audio = mono_load(file, sample_rate)
    for feature in features:
        feature_map[feature] = feature_function_map[feature](audio, sample_rate)

    return feature_map


def _file_compute_all_base_features(file, sample_rate):
    audio = mono_load(file, sample_rate)

    feature_map = {}
    feature_map['mfcc'] = base.get_mfcc(audio, sample_rate)
    feature_map['hpcp'] = base.hpcp(audio, sample_rate)
    feature_map['melody'] = base.melodia(audio, sample_rate)
    feature_map['beats'] = base.get_beats(audio, sample_rate)
    feature_map['onsets'] = base.get_onsets(audio, sample_rate)

    sone = base.bark_bands_sone(audio, sample_rate)
    feature_map['roughness'] = base.roughness(audio, sample_rate)
    feature_map['loudness'] = base.loudness(audio, sample_rate, sone)
    feature_map['sharpness'] = base.sharpness(audio, sample_rate, sone, feature_map['loudness'][1])

    return feature_map
