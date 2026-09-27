# Convert your first workflow

In this tutorial, you will convert a small CWL workflow into an OGC input
description and a JSON Schema. You need Python 3.10 or later and a terminal.

## 1. Install the library

Create a virtual environment and install cwl2ogc:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install cwl2ogc
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## 2. Create a workflow

Save this as `hello.cwl`:

```yaml
cwlVersion: v1.2
class: Workflow
id: hello
inputs:
  message:
    type: string
    label: Message
    doc: Text to pass through the workflow.
outputs:
  result:
    type: string
    outputSource: message
steps: []
```

The workflow passes one required string input directly to its output.

## 3. Convert its inputs

Save the following as `convert.py` in the same directory:

```python
import json

from cwl_utils.parser import load_document_by_uri

from cwl2ogc import BaseCWLtypes2OGCConverter

workflow = load_document_by_uri("hello.cwl")
converter = BaseCWLtypes2OGCConverter(workflow)

inputs = converter.get_inputs()
print(json.dumps(inputs, indent=2))

assert inputs["message"]["schema"] == {"type": "string"}
assert inputs["message"]["minOccurs"] == 1
assert inputs["message"]["title"] == "Message"

outputs = converter.get_outputs()
assert outputs["result"]["schema"] == {"type": "string"}
```

Run it:

```bash
python convert.py
```

The printed description includes a `message` entry with a string schema,
the title `Message`, and `minOccurs: 1`. The assertions verify that the
conversion produced the expected input and output types.

## 4. Generate a JSON Schema

Append this to `convert.py` and run it again:

```python
schema = converter.get_inputs_json_schema()
assert schema["type"] == "object"
assert schema["required"] == ["message"]
print(json.dumps(schema, indent=2))
```

This schema describes an object such as `{"message": "Hello"}`.
The `required` array records that the message must be supplied.

You have now converted both sides of a workflow and generated an input schema.
Continue with the [notebook tutorials](index.md), or follow the
[how-to guide](../how-to/json-schema.md) to save and validate schemas.
