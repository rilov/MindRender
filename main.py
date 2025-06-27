from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import Response
from pydantic import BaseModel
import subprocess
import tempfile
import os
from typing import Optional

app = FastAPI()

class MermaidRequest(BaseModel):
    mermaid_script: str
    format: Optional[str] = None  # Optional format field in body

@app.post("/render")
async def render_mermaid(
    req: MermaidRequest,
    format: str = Query('svg', regex='^(svg|png)$')
):
    # Determine format: body takes precedence over query
    fmt = req.format.lower() if req.format else format
    if fmt not in ('svg', 'png'):
        raise HTTPException(status_code=400, detail="Format must be 'svg' or 'png'")
    # Create a temporary file for the Mermaid script
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.mmd', delete=False) as mmd_file:
        mmd_file.write(req.mermaid_script)
        mmd_file.flush()
        mmd_path = mmd_file.name
    # Output file extension and content type
    if fmt == 'png':
        out_suffix = '.png'
        content_type = 'image/png'
        mmdc_args = ['-t', 'png']
    else:
        out_suffix = '.svg'
        content_type = 'image/svg+xml'
        mmdc_args = []
    with tempfile.NamedTemporaryFile(suffix=out_suffix, delete=False) as out_file:
        out_path = out_file.name
    try:
        # Call mermaid-cli (mmdc) to render
        result = subprocess.run([
            'mmdc',
            '-i', mmd_path,
            '-o', out_path,
            '--quiet',
            *mmdc_args
        ], capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=f"Mermaid render error: {result.stderr}")
        # Read output content
        with open(out_path, 'rb') as f:
            data = f.read()
        return Response(content=data, media_type=content_type)
    finally:
        # Clean up temp files
        os.remove(mmd_path)
        os.remove(out_path)

# To run: uvicorn main:app --reload
# Requires: pip install -r requirements.txt
# Also install mermaid-cli globally: npm install -g @mermaid-js/mermaid-cli 