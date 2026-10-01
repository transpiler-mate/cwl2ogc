# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import json
from pathlib import Path

import pytest
from cwl_utils.parser import LoadingOptions, Process, load_document_by_yaml
from cwl_utils.parser.cwl_v1_2 import SchemaDefRequirement, Workflow, WorkflowInputParameter
from ruamel.yaml import YAML

from cwl2ogc import BaseCWLtypes2OGCConverter

ARTIFACTS_DIR = Path("tests/artifacts")
CWL_TYPES_DIR = ARTIFACTS_DIR / "cwl-types"
CWL_TYPES_FIXTURES = [
    "inp",
    "array-inputs",
    "record",
    "exclusive-parameter-expressions",
    "complex-cwl-types",
]


def load_cwl_document(path: Path) -> Process | list[Process]:
    """Load a CWL process or graph from a fixture."""
    with path.open() as stream:
        cwl_content = YAML().load(stream)
    document = load_document_by_yaml(yaml=cwl_content, uri="io://", load_all=True)
    assert isinstance(document, (Process, list))
    return document


def load_json(path: Path) -> dict[str, dict[str, object]]:
    """Load an OGC parameter description fixture."""
    with path.open() as stream:
        document = json.load(stream)
    assert isinstance(document, dict)
    return document


def assert_conversion_matches_golden_files(fixture_name: str) -> None:
    """Check parameter names, metadata, and schema presence against fixtures."""
    workflow = load_cwl_document(CWL_TYPES_DIR / f"{fixture_name}.cwl")
    assert isinstance(workflow, Process)
    converter = BaseCWLtypes2OGCConverter(workflow)

    expected_inputs = load_json(CWL_TYPES_DIR / f"{fixture_name}_inputs.json")
    expected_outputs = load_json(CWL_TYPES_DIR / f"{fixture_name}_outputs.json")

    actual_inputs = converter._to_ogc(workflow.inputs)
    actual_outputs = converter._to_ogc(workflow.outputs)

    assert set(actual_inputs) == set(expected_inputs)
    assert set(actual_outputs) == set(expected_outputs)

    for name, expected_entry in expected_inputs.items():
        actual_entry = actual_inputs[name]
        if "title" in expected_entry:
            assert actual_entry.get("title") == expected_entry["title"]
        if "description" in expected_entry:
            assert actual_entry.get("description") == expected_entry["description"]

        expected_schema = expected_entry.get("schema", {})
        actual_schema = actual_entry.get("schema", {})
        assert isinstance(actual_schema, dict)
        if expected_schema:
            assert actual_schema

    for value in actual_inputs.values():
        assert "metadata" in value


def test_conversion_matches_golden_files() -> None:
    for fixture_name in CWL_TYPES_FIXTURES:
        assert_conversion_matches_golden_files(fixture_name)


def test_workflow_graph_conversion_for_water_bodies() -> None:
    cwl_graph = load_cwl_document(ARTIFACTS_DIR / "app-water-body.1.1.0.cwl")
    assert isinstance(cwl_graph, list)

    workflow = next(entry for entry in cwl_graph if getattr(entry, "class_", None) == "Workflow")
    converter = BaseCWLtypes2OGCConverter(workflow)

    inputs = converter.get_inputs()
    outputs = converter.get_outputs()

    assert "aoi" in inputs
    assert inputs["aoi"]["schema"]["type"] == "string"
    assert inputs["aoi"]["minOccurs"] == 1
    assert outputs["stac_catalog"]["schema"]["oneOf"]


def test_json_schema_generation_for_nullable_inputs() -> None:
    workflow = load_cwl_document(CWL_TYPES_DIR / "inp.cwl")
    assert isinstance(workflow, Process)
    converter = BaseCWLtypes2OGCConverter(workflow)

    inputs_schema = converter.get_inputs_json_schema()
    outputs_schema = converter.get_outputs_json_schema()

    assert inputs_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "example_file" in inputs_schema["$defs"]
    assert "example_file" not in inputs_schema["required"]
    assert "example_int" in inputs_schema["required"]
    assert outputs_schema["type"] == "object"


def test_dump_methods_emit_valid_json() -> None:
    workflow = load_cwl_document(CWL_TYPES_DIR / "record.cwl")
    assert isinstance(workflow, Process)
    converter = BaseCWLtypes2OGCConverter(workflow)

    streams = [io.StringIO(), io.StringIO(), io.StringIO(), io.StringIO()]
    converter.dump_inputs(streams[0], pretty_print=True)
    converter.dump_outputs(streams[1], pretty_print=True)
    converter.dump_inputs_json_schema(streams[2], pretty_print=True)
    converter.dump_outputs_json_schema(streams[3], pretty_print=True)

    for stream in streams:
        data = json.loads(stream.getvalue())
        assert isinstance(data, dict)


@pytest.mark.parametrize("requirements", [None, []])
def test_custom_type_without_requirements_does_not_crash(
    requirements: list[SchemaDefRequirement] | None,
) -> None:
    workflow = Workflow(
        id="file:///tmp/workflow.cwl#main",
        cwlVersion="v1.2",
        inputs=[
            WorkflowInputParameter(
                id="file:///tmp/workflow.cwl#main/aoi",
                type_="https://example.org/geojson.yaml#Polygon",
            )
        ],
        outputs=[],
        steps=[],
        requirements=requirements,
    )

    schema = BaseCWLtypes2OGCConverter(workflow).get_inputs_json_schema()

    assert "aoi" in schema["properties"]
    assert schema["$defs"]["aoi"] == {}


@pytest.mark.parametrize(
    ("type_name", "expected_format"),
    [
        ("Date", "date"),
        ("DateTime", "date-time"),
        ("Duration", "duration"),
        ("Email", "email"),
        ("Hostname", "hostname"),
        ("IDNEmail", "idn-email"),
        ("IDNHostname", "idn-hostname"),
        ("IPv4", "ipv4"),
        ("IPv6", "ipv6"),
        ("IRI", "iri"),
        ("IRIReference", "iri-reference"),
        ("JsonPointer", "json-pointer"),
        ("Password", "password"),
        ("RelativeJsonPointer", "relative-json-pointer"),
        ("UUID", "uuid"),
        ("URI", "uri"),
        ("URIReference", "uri-reference"),
        ("URITemplate", "uri-template"),
        ("Time", "time"),
    ],
)
@pytest.mark.parametrize("default_value", ["default-value", ""])
def test_string_format_record_default_is_unwrapped(
    type_name: str, expected_format: str, default_value: str
) -> None:
    type_uri = f"https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#{type_name}"
    # Inline the referenced record definition to keep parsing independent of network access.
    document = load_document_by_yaml(
        yaml={
            "cwlVersion": "v1.2",
            "class": "Workflow",
            "id": "file:///tmp/string-format-default.cwl#main",
            "requirements": {
                "SchemaDefRequirement": {
                    "types": [
                        {
                            "name": type_uri,
                            "type": "record",
                            "fields": [{"name": "value", "type": "string"}],
                        }
                    ]
                }
            },
            "inputs": {"formatted": {"type": type_uri, "default": {"value": default_value}}},
            "outputs": [],
            "steps": [],
        },
        uri="file:///tmp/string-format-default.cwl",
        loadingOptions=LoadingOptions(no_link_check=True),
    )
    assert isinstance(document, Process)
    converter = BaseCWLtypes2OGCConverter(document)
    expected_schema = {"type": "string", "format": expected_format, "default": default_value}

    assert converter.get_inputs()["formatted"]["schema"] == expected_schema
    assert converter.get_inputs_json_schema()["$defs"]["formatted"] == expected_schema
    assert document.inputs[0].default == {"value": default_value}


def test_ordinary_record_default_remains_an_object() -> None:
    document = load_document_by_yaml(
        yaml={
            "cwlVersion": "v1.2",
            "class": "Workflow",
            "id": "file:///tmp/ordinary-record-default.cwl#main",
            "inputs": {
                "record": {
                    "type": {
                        "type": "record",
                        "name": "OrdinaryRecord",
                        "fields": [{"name": "value", "type": "string"}],
                    },
                    "default": {"value": "default-value"},
                }
            },
            "outputs": [],
            "steps": [],
        },
        uri="file:///tmp/ordinary-record-default.cwl",
        loadingOptions=LoadingOptions(no_link_check=True),
    )
    assert isinstance(document, Process)
    converter = BaseCWLtypes2OGCConverter(document)
    expected_schema = {
        "type": "object",
        "properties": {"value": {"type": "string"}},
        "required": ["value"],
        "default": {"value": "default-value"},
    }

    assert converter.get_inputs()["record"]["schema"] == expected_schema
    assert converter.get_inputs_json_schema()["$defs"]["record"] == expected_schema
