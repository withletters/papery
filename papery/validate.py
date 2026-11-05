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

import logging
import os
import sys
import subprocess

from pykwalify.core import Core

# errors are reported by Validator itself
logging.getLogger('pykwalify').addHandler(logging.NullHandler())
logging.getLogger('pykwalify').propagate = False


class Validator:

    def __init__(self):
        pass

    def validate_config(self, config_path):
        exitflg = False
        if '.yml' in config_path or '.yaml' in config_path:
            exitflg = True if self._yamllint(config_path) else exitflg
            exitflg = True if self._pykwalify(config_path) else exitflg
        elif '.json' in config_path:
            if self._exists_cmd('jsonlint'):
                exitflg = self._jsonlint(config_path)
        if exitflg:
            sys.exit(1)

    def yamllint(self, file_list):
        exitflg = False
        pagelist = [f for f in file_list if '.yml' in f]
        for page in pagelist:
            exitflg = True if self._yamllint(page) else exitflg
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
        core = Core(source_file=file_path, schema_files=[config_path])
        core.validate(raise_exception=False)
        for error in core.validation_errors:
            print('\033[31m' + file_path + ': ' + error + '\033[0m')
            exitflg = True
        return exitflg

    def _yamllint(self, page):
        exitflg = False
        config_path = os.path.join(os.path.dirname(__file__), 'lint_configs', 'yamllint.yaml')
        results = self._execmd([sys.executable, '-m', 'yamllint', '-c', config_path, page])[0]
        for result in results:
            if not result.startswith(' '):
                filepass = result
            elif '' != result:
                res = filepass.lstrip('./') + ':' + result.lstrip(' ')
                while '  ' in res:
                    res = res.replace('  ', ' ')
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
        for (root, dirs, files) in os.walk(os.getcwd()):
            for file in files:
                target_path = os.path.join(root, file).replace("\\", "/")
                if target_path.endswith(('markdownlint.yml', 'markdownlint.yaml')):
                    config_path = target_path

        results = self._execmd('markdownlint --config ' + config_path + ' ' + page)[1]
        for result in results:
            print(result)
        return exitflg

    def _execmd(self, cmd):
        try:
            if isinstance(cmd, str):
                cmd = cmd.split()
            proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            results = [proc.stdout.splitlines(), proc.stderr.splitlines()]
        except FileNotFoundError as e:
            results = [[], [str(e.args)]]
        return results
