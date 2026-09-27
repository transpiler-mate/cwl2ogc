# CWL to OGC

cwl2ogc converts CWL workflow and tool input/output definitions into OGC API -
Processes descriptions and JSON Schema documents. Use it as a Python library or
through the transpiler-mate command-line runtime.

## Choose your next step

| Your goal | Start here |
| --- | --- |
| Learn the library with a complete example | [Tutorial: convert your first workflow](tutorials/first-conversion.md) |
| Explore arrays, records, and other CWL types | [Tutorial notebooks](tutorials/index.md) |
| Convert an application package from the command line | [Use the plugin](plugin.md) |
| Save and validate input/output schemas | [Generate JSON Schema](how-to/json-schema.md) |
| Look up Python methods | [API reference](api.md) |
| Check CLI options and output fields | [Plugin reference](reference/plugin.md) |
| Understand how CWL becomes OGC descriptions | [Conversion model](explanation/conversion-model.md) |

The documentation follows [Diátaxis](https://diataxis.fr/): tutorials support
learning, how-to guides address tasks, reference provides technical facts, and
explanation develops understanding.

Python 3.10 or later is required. The plugin is available from cwl2ogc 0.20.0.
The former standalone command was removed in 0.18.0; use
`transpiler-mate cwl2ogc` for command-line conversion.
