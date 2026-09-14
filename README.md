# cwl2ogc

[![PyPI - Version](https://img.shields.io/pypi/v/cwl2ogc.svg)](https://pypi.org/project/cwl2ogc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cwl2ogc.svg)](https://pypi.org/project/cwl2ogc)

`cwl2ogc` converts CWL workflow/tool inputs and outputs into:
- OGC API - Processes I/O descriptors
- JSON Schema documents for those I/O definitions

This is useful when publishing CWL-based application packages through OGC API - Processes interfaces.

> [!WARNING]
> Since release **0.20.0**, `cwl2ogc` is also available as a
> [transpiler-mate](https://transpiler-mate.github.io/transpiler-mate-api/) plugin.
> Use `transpiler-mate cwl2ogc` for command-line conversion; the standalone
> `cwl2ogc` command was removed in 0.18.0. The Python library remains available.
> See the [plugin guide](docs/plugin.md) for installation and usage.

## Why

The OGC API - Processes Deploy/Replace/Undeploy workflow requires a process description that exposes valid input and output metadata. `cwl2ogc` helps generate that description directly from CWL definitions.

## Installation

```bash
pip install cwl2ogc
```

Python `3.10+` is required.

## Quick Start (transpiler-mate plugin)

Install the runtime and plugin in the same Python environment:

```bash
pip install transpiler-mate-runtime "cwl2ogc>=0.20.0"
```

Generate OGC input/output descriptions from your CWL document:

```bash
transpiler-mate cwl2ogc --output processes.json workflow.cwl
```

Show command help:

```bash
transpiler-mate cwl2ogc --help
```

The output contains application metadata and a `processes` mapping keyed by
CWL process ID. See the [plugin guide](docs/plugin.md) for source requirements
and output details.

## Quick Start (Python API)

```python
from cwl_utils.parser import load_document_by_uri
from cwl2ogc import BaseCWLtypes2OGCConverter

workflow = load_document_by_uri("tests/artifacts/cwl-types/inp.cwl#inp")
converter = BaseCWLtypes2OGCConverter(workflow)

inputs = converter.get_inputs()
outputs = converter.get_outputs()

inputs_json_schema = converter.get_inputs_json_schema()
outputs_json_schema = converter.get_outputs_json_schema()
```

## Playground

Requirements:
- `docker`
- `task`

Run the published playground image:

```bash
task run-playground
```

Build and run the local playground image:

```bash
task run-playground-dev
```

Open [http://127.0.0.1](http://127.0.0.1).

## Development

Install development tooling with Hatch and run checks:

```bash
hatch run test:test-q
hatch run dev:check
hatch run dev:lint
```

Equivalent Taskfile targets:

```bash
task test
task check
task lint
```

## Documentation

Project docs: https://eoap.github.io/cwl2ogc/

Plugin and CLI docs: [docs/plugin.md](docs/plugin.md)

## Contributing

Issues and pull requests are welcome:
https://github.com/eoap/cwl2ogc/issues

### Local quality checks

Install [Hatch](https://hatch.pypa.io/) and [Taskfiles](https://taskfile.dev/docs/guide) then install the Git hook:

```console
task quality:pre-commit:install
```

Every commit runs Ruff (including the configured McCabe complexity limit),
Ruff formatting, strict mypy checks, and the pytest suite.
Run the complete hook explicitly with:

```console
task quality:pre-commit:run
```

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)
