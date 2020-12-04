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

import sys
import subprocess


class Validator(object):
    # def __init__(self):
    #     self = self

    def validate_config(config_path):
        exitflg = False

        if '.yaml' in config_path:
            cmd = 'pykwalify -d ' + config_path + ' -s config_schema.yaml'
            popen = subprocess.Popen(
                cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            popen.wait()
            results = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8').splitlines()
            # results = (popen.communicate()[1]).decode('utf-8').splitlines()
            for result in results:
                if result.startswith(' - '):
                    print('\033[31m' + 'config.yaml: ' + result + '\033[0m')
                    exitflg = True

        elif '.json' in config_path:
            cmd = 'jsonlint ' + config_path + ' -q -c'
            # results = self._cmdexe(self, cmd)
            popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            popen.wait()
            results = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8').splitlines()
            for result in results:
                if result != '':
                    print(result.replace(' line ', '').replace(', col ', ':'))

        if exitflg:
            sys.exit()

    def yamllint(file_list):
        # yamllist = [f for f in file_list if '.yaml' in file_list]
        exitflg = False
        cmd = 'yamllint .'
        popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen.wait()
        results = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8').splitlines()
        for result in results:
            if './' in result:
                filepass = result
            elif '' != result:
                res = filepass.lstrip('./') + ':' + result
                while '  ' in res:
                    res = res.replace('  ', ' ')
                if 'error' in res:
                    print('\033[31m' + res + '\033[0m')
                    exitflg = True
                else:
                    print(res)
        return exitflg

    def jsonlint(file_list):
        jsonlist = [f for f in file_list if '.json' in f]
        exitflg = False
        for page in jsonlist:
            jsoncmd = 'jsonlint ' + page + ' -q -c'
            popen = subprocess.Popen(jsoncmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            popen.wait()
            jsonresult = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8')
            if jsonresult != '':
                print('\033[31m' + jsonresult.replace('\n', '').replace(' line ', '').replace(', col ', ':') + '\033[0m')
                exitflg = True
        return exitflg

    def mdlint(file_list):
        # mdlist = [f for f in file_list if '.md' in file_list]
        exitflg = False
        cmd = 'markdownlint .'
        popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen.wait()
        results = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8').splitlines()
        for result in results:
            if 'MD013' not in result:
                print(result)
        return exitflg

    def _execmd(self, cmd):
        popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen.wait()
        results = (popen.communicate()[0] + popen.communicate()[1]).decode('utf-8').splitlines()
        return results
