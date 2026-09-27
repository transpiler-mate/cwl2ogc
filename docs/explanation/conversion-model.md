# How CWL becomes an OGC description

CWL describes executable workflows and tools. An OGC process interface needs
descriptions of the values those processes accept and return. cwl2ogc bridges
these representations by inspecting parsed CWL input and output definitions.

The converter operates on one loaded process. Loading documents, resolving
imports, and selecting a process from a graph happen before conversion. In
Python, a caller supplies the parsed process; in the command-line integration,
the transpiler-mate runtime supplies the process and application metadata.

## Two representations serve different purposes

OGC input/output descriptions combine a value schema with labels, descriptions,
and CWL type metadata. Input descriptions also include occurrence constraints
and value-passing information.

The JSON Schema methods instead describe a complete input or output object.
Parameter schemas appear under `$defs`, properties refer to those definitions,
and `required` lists parameters that are not nullable. The generated top-level
object rejects additional properties.

The plugin packages OGC descriptions together with process and application
metadata. These files support integration with an OGC service, but conversion
alone does not deploy a service or execute CWL.

## Type conversion is a translation

Primitive CWL types map to JSON-compatible types. Arrays describe their items,
records describe properties, and unions describe alternatives. File and
Directory inputs include URI and STAC representations rather than the full CWL
runtime objects. Unsupported named types produce a warning and an empty schema,
so callers should review generated descriptions for their application.

CWL `null` alternatives are represented through a `nullable` marker and optional
occurrence constraints. In generated JSON Schema, optional properties may be
omitted; the marker alone does not make JSON `null` a valid value under Draft
2020-12. Likewise, format checking depends on the validator configuration.
CWL expressions are not executed by the converter.

For runnable examples, follow the [tutorials](../tutorials/index.md). For exact
methods and current output fields, consult the [API](../api.md) and
[plugin](../reference/plugin.md) references.
