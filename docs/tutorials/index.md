# Tutorials

Start with [your first conversion](first-conversion.md). You will create a
small CWL workflow, inspect its OGC input description, and produce a JSON Schema.

## Explore the notebook examples

These worked examples load a document and display the converted inputs and
outputs. Read them in order or choose the CWL feature you want to explore.

1. [Essential input parameters](../essential-input-parameters.ipynb)
2. [Array inputs](../array-inputs.ipynb)
3. [Records and unions](../inclusive-exclusive-inputs.ipynb)
4. [Exclusive parameters with expressions](../exclusive-input-parameters-expressions.ipynb)
5. [Document graphs](../graph.ipynb)
6. [Complex CWL types](../complex-cwl-types.ipynb)
7. [Imported CWL types](../imported-cwl-types.ipynb)
8. [String formats](../string-formats.ipynb)
9. [JSON Schema generation and validation](../schema.ipynb)

To run the notebooks locally, clone the repository, install the example
dependencies, and launch Jupyter from the repository root:

```bash
python -m pip install -e . jupyterlab cwl-loader jsonschema
jupyter lab
```

Open notebooks in `docs/`. Most examples fetch CWL documents from public URLs
and require network access. The imported-types notebook also uses the checked-in
`tests/artifacts/` directory.
