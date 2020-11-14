Papery version 0.1.10

# Papery

papery is  is a simple, static site generator written in Python - supports Markdown, YAML, and JSON input and Jinja2 templating.

# Features

- Markdown and JSON as input.
- Jinja2 templating.
- Python 2 and 3 compatible.
- Embed development web server (automatic updating)

# Requirements

- [Jinja2](http://jinja.pocoo.org/)
- [markdown2](https://github.com/trentm/python-markdown2)
- [pyyaml](https://pypi.org/project/PyYAML/)

# Installation

papery is available on [pypi](https://pypi.python.org/pypi).
To get the latest released version:

    pip install papery

# Usage

## Creating new site

Run the following command

    cd path/to/your_site
    papery init

## Run with development server

    papery run

access to <http://localhost:8000> with your web browser.

All pages are automatically updated when you modified any resources.

## Build manually

    papery build

# TODO

- documentation
- validate Markdown/JSON/YAML syntax
- code syntax highlight
- create new pages via papery sub command

# License

Copyright 2013-2017 [Xcoo, Inc.][xcoo]

Licensed under the [Apache License, Version 2.0][apache-license-2.0].

[xcoo]: https://xcoo.jp
[apache-license-2.0]: http://www.apache.org/licenses/LICENSE-2.0.html
