# Plugin reference

## Command and options

```text
transpiler-mate cwl2ogc [OPTIONS] SOURCE
```

| Plugin option | Default | Meaning |
| --- | --- | --- |
| `--output PATH` | `processes.json` | JSON destination; missing parent directories are created and existing files are overwritten. |

The runtime owns source loading, process selection, metadata validation, and
shared options. Use `transpiler-mate cwl2ogc --help` to inspect the installed
command.

## Generated output

The plugin writes JSON with two-space indentation.

| Runtime context | Top-level JSON value |
| --- | --- |
| A selected `process_id` | The description of `context.resolved_process`. |
| No selected process ID | A mapping from workflow IDs to their descriptions, using `context.get_processes_by_type(Workflow)`. |

IDs are preserved as supplied by the loader and may include a URI and fragment.
There is no enclosing `processes` field.

Each process description has these fields:

| Field | Source |
| --- | --- |
| `id` | Process ID. |
| `version` | Application metadata's `software_version`. |
| `title` | Process label. |
| `description` | Process documentation. |
| `metadata` | A one-element list containing the runtime's serialized application metadata. |
| `jobControlOptions` | The string `"async-execute"`. |
| `inputs` | `BaseCWLtypes2OGCConverter.get_inputs()`. |
| `outputs` | `BaseCWLtypes2OGCConverter.get_outputs()`. |

This table describes the current serializer. The plugin generates descriptions;
it does not deploy or execute a process.

## Registration

```toml
[project.entry-points."transpiler_mate.plugins"]
cwl2ogc = "cwl2ogc.plugin:cwl2ogc"
```

`Cwl2OgcOptions` validates plugin options and forbids extra fields. The runtime
passes a `TranspilerContext` to the registered function. See the
[Python API reference](../api.md) and the
[shared plugin contract](https://transpiler-mate.github.io/transpiler-mate-api/).

For installation and conversion steps, see the [plugin how-to guide](../plugin.md).
