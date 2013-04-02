# -*- coding: utf-8 -*-
#
# Copyright (C) 2013, Xcoo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import
from __future__ import print_function, unicode_literals

import os
import shutil


def weak_tree_copy(src, dst,
                   overwrite_if_modified=True):

    def _copy(src_path, dst_path):
        print("cp %s %s" % (src_path, dst_path))
        shutil.copy(src_path, dst_path)
        shutil.copystat(src_path, dst_path)

    # Copy the media directory to the output folder
    if os.path.isdir(src):
        try:
            for root, dirs, names in os.walk(src):
                relative_root = root.replace(src, "")

                if len(relative_root) > 0 and relative_root[0] == os.sep:
                    relative_root = relative_root[1:]

                output_root = os.path.join(dst,
                                           relative_root)

                if not os.path.isdir(output_root):
                    os.mkdir(output_root)

                for d in dirs:
                    output_d = os.path.join(output_root, d)
                    if not os.path.isdir(output_d):
                        print("mkdir %s" % output_d)
                        os.mkdir(output_d)

                for n in names:
                    path = os.path.join(root, n)
                    mtime = os.path.getmtime(path)

                    output_path = os.path.join(output_root, n)

                    if not os.path.exists(output_path):
                        _copy(path, output_path)

                    if overwrite_if_modified and os.path.getmtime(output_path) < mtime:
                        _copy(path, output_path)

        except OSError:
            # Do nothing if error occured
            print('There was a problem copying the files')
