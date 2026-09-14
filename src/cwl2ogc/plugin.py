# Copyright 2026 Terradue
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

"""Built-in plugin that converts CWL input/output definitions into OGC API - Processes input/output schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from transpiler_mate.api import (
    PluginExecutionError,
    PluginFailureError,
    transpiler_plugin,
)

from cwl2ogc import BaseCWLtypes2OGCConverter

if TYPE_CHECKING:
    from cwl_utils.parser import Process
    from transpiler_mate.api import TranspilerContext


class Cwl2OgcOptions(BaseModel):
    """Options accepted by the cwl2click plugin."""

    model_config = ConfigDict(extra="forbid")

    output: Path = Field(Path("processes.json"), description="Output file path")


@transpiler_plugin(
    name="cwl2ogc",
    description="Converts CWL input/output definitions into OGC API - Processes input/output schemas.",
    options_model=Cwl2OgcOptions,
)
def cwl2ogc(context: TranspilerContext, options: Cwl2OgcOptions) -> None:
    """Serialize the resolved CWL document to ``options.output``."""
    data = context.metadata.model_dump()

    data["processes"] = {}

    def _wf_ogc_data(process: Process):
        process_data: dict[str, Any] = {}

        for attribute in ["class_", "label", "doc"]:
            if hasattr(process, attribute):
                attribute_value = getattr(process, attribute, None)
                if attribute_value:
                    process_data[attribute] = attribute_value

        try:
            cwl_converter = BaseCWLtypes2OGCConverter(process)

            process_data["inputs"] = cwl_converter.get_inputs()
            process_data["outputs"] = cwl_converter.get_outputs()
        except Exception as error:
            PluginFailureError(
                f"An unexpected error occurred while extracting schema from {process.id}: {error}"
            )

        data["processes"][process.id] = process_data

    for workflow in context.processes:
        _wf_ogc_data(workflow)

    try:
        options.output.parent.mkdir(parents=True, exist_ok=True)
        with options.output.open("w") as output_stream:
            json.dump(data, output_stream, indent=2)

        logger.success(
            f"'{context.source}' successfully converted to OGC API - Processes input/output schemas in "
            f"'{options.output.absolute()}'."
        )
    except Exception as error:
        raise PluginExecutionError(
            f"An unexpected error occurred while serializing to {options.output}"
        ) from error
