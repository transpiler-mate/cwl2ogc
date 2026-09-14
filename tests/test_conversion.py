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

from cwl_utils.parser import load_document_by_yaml
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


def load_cwl_document(path: Path):
    with path.open() as stream:
        cwl_content = YAML().load(stream)
    return load_document_by_yaml(yaml=cwl_content, uri="io://", load_all=True)


def load_json(path: Path):
    with path.open() as stream:
        return json.load(stream)


def assert_conversion_matches_golden_files(fixture_name: str):
    workflow = load_cwl_document(CWL_TYPES_DIR / f"{fixture_name}.cwl")
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


def test_conversion_matches_golden_files():
    for fixture_name in CWL_TYPES_FIXTURES:
        assert_conversion_matches_golden_files(fixture_name)


def test_workflow_graph_conversion_for_water_bodies():
    cwl_graph = load_cwl_document(ARTIFACTS_DIR / "app-water-body.1.1.0.cwl")
    assert isinstance(cwl_graph, list)

    workflow = next(
        entry for entry in cwl_graph if getattr(entry, "class_", None) == "Workflow"
    )
    converter = BaseCWLtypes2OGCConverter(workflow)

    inputs = converter.get_inputs()
    outputs = converter.get_outputs()

    assert "aoi" in inputs
    assert inputs["aoi"]["schema"]["type"] == "string"
    assert inputs["aoi"]["minOccurs"] == 1
    assert outputs["stac_catalog"]["schema"]["oneOf"]


def test_json_schema_generation_for_nullable_inputs():
    workflow = load_cwl_document(CWL_TYPES_DIR / "inp.cwl")
    converter = BaseCWLtypes2OGCConverter(workflow)

    inputs_schema = converter.get_inputs_json_schema()
    outputs_schema = converter.get_outputs_json_schema()

    assert inputs_schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "example_file" in inputs_schema["$defs"]
    assert "example_file" not in inputs_schema["required"]
    assert "example_int" in inputs_schema["required"]
    assert outputs_schema["type"] == "object"


def test_dump_methods_emit_valid_json():
    workflow = load_cwl_document(CWL_TYPES_DIR / "record.cwl")
    converter = BaseCWLtypes2OGCConverter(workflow)

    streams = [io.StringIO(), io.StringIO(), io.StringIO(), io.StringIO()]
    converter.dump_inputs(streams[0], pretty_print=True)
    converter.dump_outputs(streams[1], pretty_print=True)
    converter.dump_inputs_json_schema(streams[2], pretty_print=True)
    converter.dump_outputs_json_schema(streams[3], pretty_print=True)

    for stream in streams:
        data = json.loads(stream.getvalue())
        assert isinstance(data, dict)
