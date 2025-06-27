# MindRender: Generative AI-Powered Diagramming Tool

MindRender is a generative AI-powered diagramming tool that brings your ideas to life—instantly and visually. Just describe your system, flow, or concept in plain English, and MindRender will transform it into a clean, structured diagram using formats like Mermaid .

No dragging. No manual drawing. Just type and render.

Built for developers, architects, and creators who think in systems and communicate in visuals.

## Key Features
- Natural language to diagram conversion
- Supports formats like Mermaid and PlantUML
- Export diagrams as SVG (more export formats coming soon)
- Lightweight, responsive, and easy to use
- Perfect for documentation, whiteboarding, and technical design

## Use Cases
- Software architecture and infrastructure diagrams
- Flowcharts and process modeling
- Quick visual drafts for technical discussions
- Auto-generated diagrams for wikis or dev portals

From mind to visual in seconds — that's MindRender.

---

# Mermaid Live Preview & Diagram Generator

A modern browser-based app to write, preview, and generate [Mermaid.js](https://mermaid-js.github.io/mermaid/#/) diagrams with live rendering, OpenAI prompt integration, and export features. Includes an optional FastAPI backend for rendering diagrams as images (SVG/PNG) via API.

---

## Features
- **Live Mermaid Preview:** Paste or write Mermaid script and see the diagram update instantly.
- **Prompt-to-Diagram (OpenAI):** Describe your diagram in plain English and generate Mermaid code using OpenAI (GPT-3.5/4).
- **Download as SVG:** Export your diagram as an SVG image.
- **Dark Mode:** Toggle between light and dark themes.
- **Full-Screen Preview:** View your diagram in a full-page modal.
- **Collapsible Script Panel:** Hide/show the script editor for focused viewing.
- **Configure OpenAI Key:** Securely store your OpenAI API key in your browser (never hardcoded).
- **(Optional) FastAPI Backend:** Render Mermaid diagrams as SVG/PNG via a REST API.

---

## 1. Browser App (index.html)

### Quick Start
1. **Clone or download this repo.**
2. **Open `index.html` in your browser.**
   - No build step or server required!

### OpenAI Integration
- Click **Configure Key** and enter your OpenAI API key (starts with `sk-...`).
- Enter a prompt (e.g. `A flowchart for a login process`) and click **Generate Diagram**.
- The Mermaid script will be generated and rendered live.

#### Where is my OpenAI API key stored?
- Your API key is saved in your browser's **localStorage** under the key `openai_api_key`.
- It is **only** accessible to your browser on your computer and is **never sent to any server** or shared with others.
- To view or remove it, open your browser's developer tools and look under Local Storage, or run this in the browser console:
  ```js
  localStorage.removeItem('openai_api_key');
  ```
- **Security Note:** The key is only as secure as your local browser profile. For production, proxy OpenAI requests through your backend so the key is never exposed to the client.

### Other Features
- **Download as SVG:** Click the button to save your diagram.
- **Full-Screen Preview:** Click **Preview** to see the diagram in a modal.
- **Hide Script:** Collapse the script editor for a larger preview.
- **Dark Mode:** Toggle for a comfortable viewing experience.

---

## 2. FastAPI Backend (Optional)

This backend lets you render Mermaid diagrams as SVG or PNG images via a REST API.

### Requirements
- Python 3.8+
- Node.js (for Mermaid CLI)

### Setup
1. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Install Mermaid CLI globally:**
   ```sh
   npm install -g @mermaid-js/mermaid-cli
   ```
3. **Run the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

### API Usage
- **Endpoint:** `POST /render`
- **Body:**
  ```json
  {
    "mermaid_script": "graph TD; A-->B; B-->C;",
    "format": "svg" // or "png" (optional, default: svg)
  }
  ```
- **Response:** SVG or PNG image.

**Example with curl:**
```sh
curl -X POST "http://127.0.0.1:8000/render?format=png" \
  -H "Content-Type: application/json" \
  -d '{"mermaid_script": "graph TD; A-->B; B-->C;"}' \
  --output diagram.png
```

---

## Project Structure

```
index.html         # Main browser app (open directly)
main.py            # FastAPI backend (optional)
mcpserver.py       # MCP Model interface (for Model Context Protocol)
requirements.txt   # Python dependencies for backend
README.md          # This file
```

---

## Security & Notes
- **OpenAI API Key:** Never share your key publicly. For production, use a backend proxy.
- **Mermaid CLI:** The backend requires Node.js and the `@mermaid-js/mermaid-cli` package.
- **Browser Support:** Modern browsers only (uses ES modules).

---

## License
MIT 
