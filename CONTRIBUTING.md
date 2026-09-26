<!--
Copyright 2026 Terradue

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# Contributing to cwl2ogc

## Development setup

```bash
hatch shell
task
```

## Quality gate

Before opening a pull request, run:

```bash
task
```

## Documentation

Documentation follows Diátaxis:

- tutorials teach through guided learning;
- how-to guides solve concrete tasks;
- reference pages provide exact technical facts;
- explanation pages discuss concepts and rationale.

Place new content according to its purpose:

| Content | Location |
| --- | --- |
| Guided learning with an observable result | `docs/tutorials/` |
| Steps for a specific user task | `docs/how-to/` |
| API signatures, options, and output contracts | `docs/reference/` |
| Concepts, design decisions, and limitations | `docs/explanation/` |

Existing notebooks, `docs/plugin.md`, and `docs/api.md` retain their paths to
preserve published links. Add pages to the appropriate section in
`mkdocs.yaml` and link to related material instead of combining all four forms
on one page.

Check the documentation locally with the dependencies used by
`.github/workflows/docs.yaml`:

```bash
mkdocs build --strict
```

The documentation build executes notebooks. Their example dependencies include
`cwl-loader` and `jsonschema`, and remote examples require network access.
