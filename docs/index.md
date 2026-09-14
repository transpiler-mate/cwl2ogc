# CWL Workflow inputs/outputs to OGC API Processes inputs/outputs

!!! warning "transpiler-mate plugin available since 0.20.0"

    Since release **0.20.0**, `cwl2ogc` is also available as a
    [transpiler-mate](https://transpiler-mate.github.io/transpiler-mate-api/) plugin.
    Use `transpiler-mate cwl2ogc` for command-line conversion; the standalone
    `cwl2ogc` command was removed in 0.18.0. The Python library remains available.
    Follow the [plugin guide](plugin.md) for installation, usage, and output details.

The OGC API - Processes Part 2: Deploy, Replace, Undeploy (DRU) specification enables the deployment of executable Application Packages, such as CWL workflows, as processing services. 

A key part of the deploy operation involves parsing the CWL document to generate an OGC-compliant process description, exposing the workflow’s inputs and outputs.

The **cwl2ogc** Python library is a helper library to automate the conversion of CWL input/output definitions into OGC API - Processes input/output schemas.

## The library:

* Parses a CWL Workflow document.

* Extracts and interprets its inputs and outputs.

* Converts them to the structure required for input and output definitions in OGC API - Processes (JSON Schema-like structure, including metadata such as title, description, schema, etc.).

* Supports common CWL types (File, Directory, string, int, float, arrays, optional types, custom types etc.) and map them to OGC API Process I/O types.

* Handles CWL input binding attributes (e.g., default values, required vs. optional) to enrich the process description.

Provides utilities to assist with:

* `GET /processes/{id}` (i.e. process description generation)

* `POST /processes` (i.e. deployment flow)

This library may be useful for OGC API - Processes implementations that support deploying CWL Workflows as execution units, helping bridge the gap between CWL syntax and the standardized OGC process interface.Parsing

## Parsing

Just instantiate a `cwl2ogc.BaseCWLtypes2OGCConverter` object, passing the parsed CWL using various availabe APIs:

- [cwl-utils](https://github.com/common-workflow-language/cwl-utils);
- [cwltool](https://github.com/common-workflow-language/cwltool);
- [cwl-loader](https://terradue.github.io/cwl-loader/).

## Serializing

Once the document is parsed, invoke the

* `cwl2ogc.BaseCWLtypes2OGCConverter.dump_inputs`,
* `cwl2ogc.BaseCWLtypes2OGCConverter.dump_outputs`.

APIs to dump the CWL inputs/outputs to the target Stream (i.e. a file, the stdout, ...) in OGC JSON format.

## JSON Schema

Once the document is parsed, invoke the

* `cwl2ogc.BaseCWLtypes2OGCConverter.dump_inputs_json_schema`,
* `cwl2ogc.BaseCWLtypes2OGCConverter.dump_outputs_json_schema`.

APIs to dump the CWL inputs/outputs to the target Stream (i.e. a file, the stdout, ...) in JSON Schema format, see the live [schema](./schema/) sample to check how to validate inputs/outputs.
