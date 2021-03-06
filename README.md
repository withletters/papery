[![PyPI version](https://badge.fury.io/py/papery.svg)](https://badge.fury.io/py/papery)

# Papery

Static site generator with Jinja2 templates and structured content in Markdown, YAML, and JSON

# Features

- Describe content with Markdown, YAML, and JSON
- Jinja2 templating

# Requirements

- [Jinja2](http://jinja.pocoo.org/)
- [markdown2](https://github.com/trentm/python-markdown2)
- [pyyaml](https://pypi.org/project/PyYAML/)

# Installation

papery is available on [pypi](https://pypi.python.org/pypi).

```console
pip install papery
```

# Usage

## Creating a new site

Run the following command

```console
cd path/to/your_site/directory
papery init
```

## Run with the development server

```console
papery run
```

You can see your web site via <http://localhost:8000>. All pages are automatically updated when you modified any resources.

## Build manually

```console
papery build
```

# TODO

- documentation
- validate Markdown, JSON, and YAML syntax
- code syntax highlight
- styling with SASS/SCSS

# License

Copyright 2013-2020 [Xcoo, Inc.][xcoo]

Licensed under the [Apache License, Version 2.0][apache-license-2.0].

[xcoo]: https://xcoo.com
[apache-license-2.0]: http://www.apache.org/licenses/LICENSE-2.0.html
