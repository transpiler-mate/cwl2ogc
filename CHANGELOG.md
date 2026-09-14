# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.20.0] - 2026-09-14

### Added

- `cwl2ogc` is available as a [transpiler-mate](https://transpiler-mate.github.io/transpiler-mate-api/) plugin.

## [0.19.0] - 2026-07-28

### Changed

- `cwl-utils` dependency bumped to `v0.42`

### Added

- Stronger code chekers with Ruff+McCabe & Bandit

## [0.18.0] - 2026-05-13

### Removed

- Removed the built-in CLI and generated CLI documentation; CLI functionality is being migrated to `transpiler-mate`.
- Removed CLI-oriented tests and package configuration tied to the old command entry point.

### Fixed

- Removed an unused `click.testing.CliRunner` import so Ruff checks stay clean.

## [0.17.0] - 2026-05-12

### Added

- Enriched CLI-generated output metadata via `transpiler-mate`.

### Changed

- Reused the remote quality Taskfile configuration to avoid duplicating quality tasks locally.

### Fixed

- Handled CWL inputs without metadata in the test fixtures.
- Fixed broken lint checks.

## [0.16.0] - 2026-04-10

### Fixed

- Corrected `TypeAlias` detection by checking whether type arguments are present.

## [0.15.0] - 2026-04-08

### Added

- Added support for mapping CWL `Directory` values to GeoJSON `FeatureCollection` schemas.

## [0.14.0] - 2026-04-07

### Added

- Added Dependabot configuration for automated dependency updates.

### Changed

- Updated GitHub Actions workflow dependencies, including `actions/checkout` and `actions/setup-python`.
- Refreshed release preparation metadata for the next package version.

## [0.13.0] - 2026-03-06

### Added

- Added unit tests for conversion behavior.

### Changed

- Updated the README with current usage and development guidance.
- Applied Ruff linting updates.

## [0.12.0] - 2026-02-05

### Added

- First tagged release, consolidating earlier untagged development from project initialization through `0.12.0`.
- Added the core CWL-to-OGC conversion library for OGC API - Processes input and output descriptors.
- Added JSON Schema generation for CWL inputs and outputs, including separate input and output schema generation.
- Added Python APIs to return descriptors in memory and stream input/output JSON representations.
- Added support for CWL metadata, `minOccurs`, `maxOccurs`, `valuePassing`, array handling, records, command output records, command output parameters, `long` values, and missing requirements guards.
- Added schema support for Directory/File by-value and by-reference handling, STAC Items, and STAC Collections.
- Added an initial CLI, playground, documentation notebooks, generated API documentation, CI workflows, package workflows, and test coverage.

### Changed

- Avoided serializing large STAC Item and Collection schemas by referencing their public schema documents.
- Updated the `cwl-utils` dependency.
- Reworked parsing and converter APIs, removed redundant CWL documents, regenerated notebooks, improved typing, and streamlined documentation.
- Relicensed the project to Apache-2.0 and refreshed copyright headers.

### Fixed

- Fixed record `name`/`id` handling and missing output schema support.
- Fixed the STAC Item public schema URL.
- Fixed a Python `cgi` import issue, pdoc installation, import organization, f-string syntax, documentation links, and CI/package workflow issues.

[unreleased]: https://github.com/eoap/cwl2ogc/compare/v0.20.0...HEAD
[0.20.0]: https://github.com/eoap/cwl2ogc/compare/v0.19.0...v0.20.0
[0.19.0]: https://github.com/eoap/cwl2ogc/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/eoap/cwl2ogc/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/eoap/cwl2ogc/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/eoap/cwl2ogc/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/eoap/cwl2ogc/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/eoap/cwl2ogc/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/eoap/cwl2ogc/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/eoap/cwl2ogc/releases/tag/v0.12.0
