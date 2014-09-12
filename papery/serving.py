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

from __future__ import print_function, unicode_literals

import os

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import SimpleHTTPRequestHandler  # NOQA

try:
    from SocketServer import TCPServer as HTTPServer
except ImportError:
    from http.server import HTTPServer  # NOQA


# TODO(takashi) refactor


class Server(object):

    def __init__(self, root_dir=None, host='', port=8000,
                 watch_dirs=[], change_handler=None):
        self.root_dir = os.path.abspath(root_dir)
        self.host = host
        self.port = port
        self.watch_dirs = [os.path.abspath(d) for d in watch_dirs]
        self.change_handler = change_handler

        self.work_dir = os.getcwd()

    def run(self):
        if self.root_dir:
            os.chdir(self.root_dir)

        wrap = RebuildHandlerWrapper(self.change_handler, self.watch_dirs,
                                     self.work_dir)
        req_handler = wrap.request_handler

        HTTPServer.allow_reuse_address = True

        server = HTTPServer((self.host, self.port), req_handler)
        socket_info = server.socket.getsockname()

        print("Starting dev server on http://%s:%s... (Ctrl-C to stop)"
              % (socket_info[0], socket_info[1]))
        print("Serving files from", self.root_dir)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping development server...")
        finally:
            server.shutdown()


class RebuildHandlerWrapper(object):

    def __init__(wrap_self, rebuild, watch_dirs, work_dir):
        """
        We can't pass arugments to HTTPRequestHandlers, because HTTPServer
        calls __init__. So make a closure.
        """
        wrap_self.rebuild = rebuild
        wrap_self.watch_dirs = watch_dirs
        wrap_self.work_dir = work_dir

        wrap_self._modtime_sum = None
        wrap_self.changed()

        class RebuildHandler(SimpleHTTPRequestHandler):
            """Rebuild if something has changed."""

            timeout = 30

            def setup(self):
                "Sets a timeout on the socket"
                self.request.settimeout(self.timeout)
                SimpleHTTPRequestHandler.setup(self)

            def handle(self):
                """
                Handle a request and, if anything has changed, rebuild the
                site before responding.
                """
                if wrap_self.changed():
                    current_dir = os.getcwd()
                    os.chdir(wrap_self.work_dir)
                    wrap_self.rebuild()
                    os.chdir(current_dir)

                SimpleHTTPRequestHandler.handle(self)

        wrap_self.request_handler = RebuildHandler

    def _sum_modified_time(self, scan_dirs):
        t = 0

        for d in scan_dirs:
            for root, dirs, files in os.walk(d):
                for f in files:
                    if not f.startswith('.'):
                        abspath = os.path.join(root, f)
                        t += os.stat(abspath).st_mtime

                sub_dirs = []
                for sub_d in dirs:
                    if not sub_d.startswith('.'):
                        sub_dirs.append(os.path.join(root, sub_d))

                if len(sub_dirs) > 0:
                    t += self._sum_modified_time(sub_dirs)

        return t

    def changed(self):
        """
        Returns if the contents of the monitored directories have changed since
        the last call. It will return always return false on first run.
        """
        last_modtime_sum = self._modtime_sum

        # calculate simple sum of file modification times
        self._modtime_sum = self._sum_modified_time(self.watch_dirs)

        if last_modtime_sum is None:
            # always return false on first run
            return False
        else:
            # otherwise return if file modification sums changed since last run
            return (last_modtime_sum != self._modtime_sum)
