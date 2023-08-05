# Connexion Compose

## Purpose

Create Connexion schema composed from several files in a nested directory structure.

Resulting schema automatically includes common defaults, which you can use or override.

Requires Python 3.7+

## Installation

```
pip install connexion-compose
```

## Usage

```python
from connexion_compose import compile_schema

spec_dir = 'some/dir'

schema = compile_schema(spec_dir)
```

The `compile_schema` function traverses the specification directory and all subdirectories,
creating YAML attributes according to the directory structure.
The bottom level files are "headers" and top level features, usually all contained in headers.py.

For example, given the following directory structure:

```
├── 10-header.yml
├── 90-footer.yml
├── definitions
│   └── 50-whatever.yml
├── parameters
│   ├── 10-par1.yml
│   └── 20-par2.yml
└── x
    └── y
        └── z.yml
```

The resulting object will correspond to the following YAML input:

```
[contents of 10-header.yml]
[contents of 90-footer.yml]
definitions:
  [contents of 50-whatever.yml]
parameters:
  [contents of 10-par1.yml]
  [contents of 20-par2.yml]
x:
  y:
    [contents of z.yml]
```

# Defaults

```yaml
swagger: '2.0'
info:
  contact: {name: Please add a contact name}
  description: Please add a description
  title: Please add a title
  version: 0.0.0
  x-visibility: unlisted
basePath: /
schemes: [https]
consumes: [application/json]
produces: [application/json]
definitions:
  Currency: {format: iso_4217, type: string}
  Decimal: {format: decimal, type: string}
  Path: {format: path, type: string}
  Timestamp: {format: rfc_3339, type: string}
  URL: {format: url, type: string}
  UUID: {format: uuid, type: string}
```
