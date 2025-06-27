# mcpserver.py
# Expose the FastAPI app for MCP or any ASGI server

from main import app 

import subprocess
import tempfile
import os

class Model:
    def __init__(self, context):
        self.tools = [
            {
                "name": "render_mermaid",
                "description": "Render a Mermaid script as SVG or PNG.",
                "parameters": {
                    "mermaid_script": {"type": "string", "description": "The Mermaid diagram script."},
                    "format": {"type": "string", "enum": ["svg", "png"], "default": "svg", "description": "Output format (svg or png)"}
                }
            }
        ]

    def predict(self, inputs, context=None):
        """
        Expects inputs = {'mermaid_script': '...', 'format': 'svg' or 'png'}
        Returns: {'image': <bytes>, 'content_type': 'image/svg+xml' or 'image/png'}
        """
        script = inputs.get('mermaid_script', '')
        fmt = inputs.get('format', 'svg')
        if fmt not in ('svg', 'png'):
            fmt = 'svg'
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.mmd', delete=False) as mmd_file:
            mmd_file.write(script)
            mmd_file.flush()
            mmd_path = mmd_file.name
        out_suffix = '.png' if fmt == 'png' else '.svg'
        content_type = 'image/png' if fmt == 'png' else 'image/svg+xml'
        mmdc_args = ['-t', 'png'] if fmt == 'png' else []
        with tempfile.NamedTemporaryFile(suffix=out_suffix, delete=False) as out_file:
            out_path = out_file.name
        try:
            result = subprocess.run([
                'mmdc',
                '-i', mmd_path,
                '-o', out_path,
                '--quiet',
                *mmdc_args
            ], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Mermaid render error: {result.stderr}")
            with open(out_path, 'rb') as f:
                data = f.read()
            return {'image': data, 'content_type': content_type}
        finally:
            os.remove(mmd_path)
            os.remove(out_path) 