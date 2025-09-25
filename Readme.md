# Offline-DevOps-Agent-with-LLM-Brain

Offline-DevOps-Agent-with-LLM-Brain is an offline-first DevOps automation agent
that can analyze logs, run small automated tasks, and (optionally) call a
locally-hosted LLM brain. The goal is to provide useful automation while
remaining network-independent.
This README covers quickstart steps, the mock LLM server, the local
Transformers backend (local-only), tests, and CI.

## Quickstart (minimum)
Create a Python virtual environment and install minimal test deps:

```powershell
Run the built-in analyzer on a path (example uses the sample `logs/`):

```powershell
If you want a quick demo, create a small sample log and run the command:

```powershell
## Mock LLM server (for dev & tests)

We provide a tiny HTTP mock server useful for development and integration
Start the server (local):

```powershell
Query it (example using PowerShell / curl):

```powershell
The mock server is used by our tests and is safe to run locally.

## Transformers local backend (optional)
The project includes a `LocalLLM` adapter that can load a Hugging Face
compatible causal LM from a local model directory. This is optional and the
project will work without it (the adapter is lazily imported).
Notes and requirements:

- You must obtain and place the model files locally (no automatic downloads).
- Install heavy deps to use this backend:

```powershell
- Run a query against a local model directory:

```powershell
If the model files are missing or incompatible the adapter will print a
helpful error. We intentionally do not download models for you.

## CLI
The main CLI (`src/main.py`) supports:

- `--analyze-logs <path>`: analyze a file or directory of logs
- `--run-task <task-name>`: run the simple agent task (simulated)
- `--model-path <dir>`: path to local HF model (used with `--query`)
- `--query "prompt"`: run the LLM on this prompt
- `--max-tokens`, `--temperature`

Example: analyze logs and then query the LLM
```powershell
python -m src.main --analyze-logs .\logs
python -m src.main --model-path C:/models/your-model --query "Summarize these logs" --max-tokens 100

## Tests
- Unit tests are in `tests/` and use `pytest`.
- Run all tests locally:

```powershell
We include mocked tests for the LLM so CI does not need heavy dependencies.

## CI
We provide a GitHub Actions workflow at `.github/workflows/ci.yml`:

- Fast test matrix on Python 3.11/3.12/3.13 runs on PRs and push to `main`.
- An optional heavy job installs `transformers` and `torch` and runs a small
	smoke test; this runs on pushes to `main` (adjustable in the workflow).

## Model placement & licensing
- You must obtain any model artifacts yourself and ensure you have the right
	to use them. Place the model in a directory and point `--model-path` there.
- Many models require significant RAM/VRAM; prefer quantized GGUF models
	for CPU-only deployments (see project docs and model vendor guidance).

## Next steps / suggestions
- Add additional backends (llama.cpp / ggml) for CPU-friendly inference.
- Add more robust safety filtering and prompt sanitization before using
	any LLM in production.

## Contributing
- Fork, create a branch, make changes, run tests, and open a pull request.

## License
This project is MIT licensed. See the `LICENSE` file for details.

## Contact
Chetan Bhargav – https://github.com/chetanjohan

# Offline-DevOps-Agent-with-LLM-Brain

## Overview
**Offline-DevOps-Agent-with-LLM-Brain** is an offline-first DevOps automation agent powered by a local Large Language Model (LLM) brain. It is designed to help developers and system administrators analyze logs, automate workflows, and perform system operations without relying on internet connectivity.

This project focuses on modularity, extensibility, and offline efficiency.

---

## Features
- **Offline LLM Brain**: Run a lightweight LLM locally to understand system logs and commands.  
- **Workflow Automation**: Automate repetitive DevOps tasks with customizable modules.  
- **Log Analysis**: Parse and analyze logs from Docker, system services, and custom applications.  
- **Pluggable Modules**: Easily extend with new offline tools and scripts.  
- **CLI Interface**: Interact with the agent via a command-line interface.

---

## Project Structure
\`\`\`
Offline-DevOps-Agent-with-LLM-Brain/
├── src/
│   ├── main.py            # CLI entry point
│   ├── agent/             # Core agent modules
│   ├── optimizer/         # Workflow optimizers
│   └── analyzer/          # Log and data analysis modules
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── README.md              # Project overview
\`\`\`

---

## Installation
1. Clone the repository:
\`\`\`bash
git clone https://github.com/<your-username>/Offline-DevOps-Agent-with-LLM-Brain.git
cd Offline-DevOps-Agent-with-LLM-Brain
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

---

## Usage
Run the agent via the CLI:
\`\`\`bash
python src/main.py --help
\`\`\`
Typical workflow commands:
\`\`\`bash
python src/main.py analyze-logs --path /var/log/
python src/main.py run-task --task deploy_app
\`\`\`

---

## Contributing
Contributions are welcome!  
- Fork the repository  
- Create a new branch (\`git checkout -b feature-name\`)  
- Make changes and commit (\`git commit -m "Add feature"\`)  
- Push the branch and open a pull request  

---

## License
This project is licensed under the MIT License. See the \`LICENSE\` file for details.

---

## Contact
Chetan Bhargav – [GitHub](https://github.com/chetanjohan) – [LinkedIn](https://www.linkedin.com/in/chetan-srivatsa-15137936a)
EOL
