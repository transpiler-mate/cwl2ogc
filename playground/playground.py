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

import os
import json
import streamlit as st
from cwl2ogc import load_converter_from_string_content
from code_editor import code_editor
import tempfile
from io import StringIO
import yaml
from cwltool.main import main as cwltool

st.header("CWL to OGC API Processes inputs/outputs")
st.set_page_config(layout="wide")


def validate_cwl(cwl_content):
    """Checks whether the CWL file meets basic conformance criteria.

    Returns
    -------
    tuple
        A tuple containing the return value of cwltool and
        the stdout and stderr content
    """
    temp_dir = tempfile.mkdtemp()
    temp_cwl_path = os.path.join(temp_dir, "temp_cwl")

    with open(temp_cwl_path, "w") as outfile:
        yaml.dump(cwl_content, outfile, default_flow_style=False)

    out = StringIO()
    err = StringIO()
    res = cwltool(
        ["--validate", temp_cwl_path],
        stderr=out,
        stdout=err,
    )
    os.remove(temp_cwl_path)

    return res, out.getvalue(), err.getvalue()


btn_settings_editor_btns = [
    {
        "name": "copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": ["copyAll"],
        "style": {"top": "0rem", "right": "0.4rem"},
    },
    {
        "name": "update",
        "feather": "RefreshCw",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0rem", "right": "0.4rem"},
    },
]

with open(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources/custom_buttons_bar_alt.json",
    )
) as json_button_file_alt:
    custom_buttons_alt = json.load(json_button_file_alt)

height = [22, 25]
language = "yaml"
theme = "default"
shortcuts = "vscode"
focus = False
wrap = True
btns = custom_buttons_alt

example_cwl = """\
cwlVersion: v1.2
class: CommandLineTool
id: array-inputs
inputs:
  filesA:
    label: filesA label
    doc: filesA doc
    type: string[]
    inputBinding:
      prefix: -A
      position: 1

  filesB:
    label: filesB label
    doc: filesB doc
    type:
      type: array
      items: string
      inputBinding:
        prefix: -B=
        separate: false
    inputBinding:
      position: 2

  filesC:
    label: filesC label
    doc: filesC doc
    type: string[]
    inputBinding:
      prefix: -C=
      itemSeparator: ","
      separate: false
      position: 4

outputs:
  example_out:
    type: stdout
stdout: output.txt
baseCommand: echo
"""

ace_props = {"style": {"borderRadius": "0px 0px 8px 8px"}}
response_dict = code_editor(
    example_cwl,
    height=height,
    lang=language,
    theme=theme,
    shortcuts=shortcuts,
    focus=focus,
    buttons=btns,
    props=ace_props,
    options={"wrap": wrap},
    allow_reset=True,
    key="code_editor_demo",
)

if response_dict["type"] == "submit":
    cwl_content = response_dict["text"]

    try:
        res, out, err = validate_cwl(yaml.load(cwl_content, Loader=yaml.FullLoader))

        if res != 0:
            st.error(f"Validation failed with error code {res}.")
            st.text_area("Validation Output", value=out, height=10)
            st.text_area("Validation Error", value=err, height=300)
            st.stop()

        converter = load_converter_from_string_content(cwl_content)

        inputs = converter.get_inputs()
        outputs = converter.get_outputs()
        inputs_schema = converter.get_inputs_json_schema()
        outputs_schema = converter.get_outputs_json_schema()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Inputs OGC definition")
            st.json(inputs)

        with col2:
            st.subheader("Outputs OGC definition")
            st.json(outputs)

        with col3:
            st.subheader("Inputs JSON schema")
            st.json(inputs_schema)

        with col4:
            st.subheader("Outputs JSON schema")
            st.json(outputs_schema)

    except Exception as e:
        st.error(f"Error parsing CWL: {e}")
