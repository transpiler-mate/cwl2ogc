# Generate and validate JSON Schema

Use the Python API to save separate schemas for a parsed CWL process. Install
`cwl2ogc` and, for the validation step, `jsonschema`:

```bash
python -m pip install cwl2ogc jsonschema
```

## Load a process and save its schemas

Replace `workflow.cwl` with your document. For a graph, include the selected
process fragment, for example `workflow.cwl#main`.

```python
from pathlib import Path

from cwl_utils.parser import load_document_by_uri

from cwl2ogc import BaseCWLtypes2OGCConverter

workflow = load_document_by_uri("workflow.cwl")
converter = BaseCWLtypes2OGCConverter(workflow)

with Path("inputs.schema.json").open("w") as stream:
    converter.dump_inputs_json_schema(stream, pretty_print=True)
with Path("outputs.schema.json").open("w") as stream:
    converter.dump_outputs_json_schema(stream, pretty_print=True)
```

The files are overwritten if they already exist. To save OGC parameter
descriptions instead, use `dump_inputs()` and `dump_outputs()`.

## Validate values

Save your input values as `inputs.json`, then validate them against the
generated input schema:

```python
import json
from pathlib import Path

from jsonschema import Draft202012Validator

with Path("inputs.schema.json").open() as stream:
    schema = json.load(stream)
with Path("inputs.json").open() as stream:
    values = json.load(stream)

Draft202012Validator.check_schema(schema)
Draft202012Validator(schema).validate(values)
```

Successful validation returns without output. Invalid values raise
`jsonschema.exceptions.ValidationError`; an invalid schema raises
`jsonschema.exceptions.SchemaError`.

Use the output schema in the same way to validate output values. Schemas for
File and Directory values can contain external references, whose resolution
must be supported by your validator configuration. See the
[conversion model](../explanation/conversion-model.md) for nullability and
format limitations, and the [API reference](../api.md) for all converter methods.
