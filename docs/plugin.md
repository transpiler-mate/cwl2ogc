# Convert an application package with the plugin

Use this guide when you have a CWL application package and want to write OGC
process descriptions from the command line.

## Install the runtime and plugin

Install both packages in the same Python 3.10+ environment:

```bash
python -m pip install transpiler-mate-runtime "cwl2ogc>=0.20.0"
transpiler-mate cwl2ogc --help
```

The runtime discovers the installed plugin automatically.

## Convert your package

The source must satisfy the runtime's application metadata requirements.
Consult the [runtime documentation](https://terradue.github.io/transpiler-mate-runtime/)
for source adapters, metadata validation, and shared options.

Replace `workflow.cwl` with your application package:

```bash
transpiler-mate cwl2ogc --output build/processes.json workflow.cwl
```

The plugin creates missing parent directories and overwrites an existing output
file. Without a selected process ID, the output maps workflow IDs to process
descriptions.

To convert a selected process, include its fragment in the source:

```bash
transpiler-mate cwl2ogc --output build/main.json 'workflow.cwl#main'
```

When the runtime supplies a selected process ID, the plugin writes that process
description directly. See the [output reference](reference/plugin.md#generated-output)
for the two document shapes.

## Migrate from the former CLI

The standalone `cwl2ogc` executable was removed in 0.18.0. Install the runtime
and use `transpiler-mate cwl2ogc` instead. Replace the former `--workflow-id`
option with a source fragment and update consumers to use the current
[output structure](reference/plugin.md#generated-output).

For separate input/output JSON Schema files, use the
[Python schema guide](how-to/json-schema.md).
