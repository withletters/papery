# -*- coding: utf-8 -*-
#
# Copyright (C) 2020, Xcoo, Inc.
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
import sys
import subprocess


class Validator(object):

    def __init__(self):
        pass

    def validate_config(self, config_path):
        exitflg = False
        if '.yaml' in config_path:
            if self._exists_cmd('yamllint'):
                exitflg = True if self._yamllint(config_path) else exitflg
            if self._exists_cmd('pykwalify'):
                exitflg = True if self._pykwalify(config_path) else exitflg
        elif '.json' in config_path:
            if self._exists_cmd('jsonlint'):
                exitflg = self._jsonlint(config_path)
        if exitflg:
            sys.exit()

    def yamllint(self, file_list):
        exitflg = False
        if self._exists_cmd('yamllint'):
            pagelist = [f for f in file_list if '.yaml' in f]
            for page in pagelist:
                exitflg = True if self._yamllint(page) else exitflg
        return exitflg

    def jsonlint(self, file_list):
        exitflg = False
        if self._exists_cmd('jsonlint'):
            pagelist = [f for f in file_list if '.json' in f]
            for page in pagelist:
                exitflg = True if self._jsonlint(page) else exitflg
        return exitflg

    def mdlint(self, file_list):
        exitflg = False
        if self._exists_cmd('markdownlint'):
            pagelist = [f for f in file_list if '.md' in f]
            for page in pagelist:
                exitflg = True if self._markdownlint(page) else exitflg
        return exitflg

    def _exists_cmd(self, cmd):
        results = self._execmd(cmd + ' --version')[0]
        if results:
            return True
        else:
            print('command not found: ' + cmd)
            return False

    def _pykwalify(self, file_path):
        exitflg = False
        config_path = os.path.join(os.path.dirname(__file__), 'lint_configs', 'config_schema.yaml')
        cmd = 'pykwalify -d ' + file_path + ' -s ' + config_path
        results = sum(self._execmd(cmd), [])
        for result in results:
            if result.startswith(' - '):
                print('\033[31m' + 'config.yaml: ' + result + '\033[0m')
                exitflg = True
        return exitflg

    def _yamllint(self, page):
        exitflg = False
        config_path = os.path.join(os.path.dirname(__file__), 'lint_configs', 'yamllint.yaml')
        results = self._execmd('yamllint -c ' + config_path + ' ' + page)[0]
        for result in results:
            if not result.startswith(' '):
                filepass = result
            elif '' != result:
                res = filepass.lstrip('./') + ':' + result.lstrip(' ')
                while '  ' in res: res = res.replace('  ', ' ')
                if 'error' in res:
                    print('\033[31m' + res + '\033[0m')
                    exitflg = True
                else:
                    print(res)
        return exitflg

    def _jsonlint(self, page):
        exitflg = False
        results = self._execmd('jsonlint ' + page + ' -q -c')[1]
        for result in results:
            print('\033[31m' + result.replace(' line ', '').replace(', col ', ':') + '\033[0m')
            exitflg = True
        return exitflg

    def _markdownlint(self, page):
        exitflg = False
        config_path = os.path.join(os.path.dirname(__file__), 'lint_configs', 'markdownlint.yaml')
        results = self._execmd('markdownlint --config ' + config_path + ' ' + page)[1]
        for result in results:
            print(result)
        return exitflg

    def _execmd(self, cmd):
        try:
            popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            popen.wait()
            cmd_result = popen.communicate()
            results = [cmd_result[0].decode('utf-8').splitlines(),
                       cmd_result[1].decode('utf-8').splitlines()]
        except FileNotFoundError as e:
            results = [[], [str(e.args)]]
        return results
