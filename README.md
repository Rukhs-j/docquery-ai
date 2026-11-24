# DocQuery AI — Python

A user-isolated document question-answering service with chunking, retrieval, source excerpts and optional local model generation.

This is the Python/FastAPI conversion of the Java portfolio project. It includes a browser UI, REST API, local persistence, sample inputs, tests and optional model integration where relevant.

## Implemented features

- Paste documents or upload UTF-8 .txt/.md files; file limit 40000 bytes.
- 750-character chunks with a 600-character step.
- Access filtering occurs in SQL before keyword or vector scoring.
- Demo mode returns keyword-ranked evidence; Ollama mode uses real embeddings, cosine similarity and model-generated answers.
- Documents, chunks and vectors persist in SQLite; delete removes the associated chunks.

## Run the Windows-ready suite

If you downloaded **All-Python-Projects-Windows-Ready.zip**:

1. Extract the whole ZIP. Keep the shared **runtime** folder beside the five project folders.
2. Open **docquery-ai**.
3. Double-click **start.bat**.
4. Wait for application startup, then open **http://localhost:8083**.
5. Keep the terminal open; press Ctrl+C to stop.

The Windows x64 suite includes a private Python 3.13.17 runtime and pinned dependencies. It does not modify your system Python or PATH, and the default demo does not need internet, a database server, Java, API keys or a model account.

## Run the individual source ZIP

Install **Python 3.11+**. The first dependency installation needs internet.

Windows: double-click **start.bat**. It creates .venv and installs requirements if a shared runtime is unavailable.

Manual setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

macOS/Linux: run **sh start.sh**, or create a virtual environment and run python run.py yourself.

Interactive API documentation: **http://localhost:8083/docs**. The Swagger UI uses external CDN assets and may need internet; the main project UI and /openapi.json work without those assets.

To change the port in PowerShell:

```powershell
$env:PORT="9090"
.\start.bat
```

## Demo accounts

| User | Password | Role |
| --- | --- | --- |
| alice | demo-pass | Customer/user |
| bob | demo-pass | Separate customer/user |
| agent | demo-pass | Support engineer |
| admin | demo-pass | Administrator |

Start as **alice** in the UI. The API uses HTTP Basic authentication with a synthetic fixed demo password. PBKDF2 is used for comparison, but this is not production identity management.

## Try the project

1. As alice, ask what expense reimbursement requires and inspect the policy source.
2. Switch to bob and verify that Alice's document is not accessible.
3. Upload samples/expense-policy.txt or paste your own document.
4. Ask a question containing a distinctive term from it.
5. Ask qzxunobtainium to inspect the no-evidence response.
6. Delete your document and verify retrieval no longer includes it.

## API reference

All /api endpoints require authentication.

| Method | Route | Purpose |
| --- | --- | --- |
| GET/POST | /api/documents | List/add documents; POST {title,text} |
| POST | /api/documents/upload | Multipart field file, .txt/.md only |
| DELETE | /api/documents/{id} | Delete own document and chunks |
| POST | /api/search | Retrieve with {question} |
| POST | /api/ask | Retrieve and answer with {question} |

Database-backed responses retain **UPPERCASE** keys to preserve the existing UI contract. AI responses use camelCase.

Example in PowerShell:

```powershell
$auth=[Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("alice:demo-pass"))
$headers=@{Authorization="Basic $auth"}
$body='{"question":"What is required for expense reimbursement?"}'
Invoke-RestMethod -Uri "http://localhost:8083/api/ask" -Method Post -Headers $headers -ContentType "application/json" -Body $body
```

Creation returns 200. Input errors return 400, missing records 404, access violations 403, conflicts 409 and configured simulation failures 422/503. Requests declaring more than 256000 bytes are rejected with 413.

## Source code structure

```text
application.py       Routes and create_app factory
services.py          Project-specific models and business rules
core.py              SQLite, demo authentication, retrieval, Ollama adapter
factory.py           Lifespan, worker, errors and static UI
run.py               Application entry point
run_tests.py         Test entry point
requirements.txt     Pinned dependencies
static/              Browser UI; no npm build
tests/               pytest behavior and adapter tests
samples/             Synthetic example inputs
docs/                AI setup, conversion notes and verification
```

Stack: Python, FastAPI, Pydantic, SQLite, httpx, Uvicorn and pytest. Standard-library SQL is used directly; SQLAlchemy and LangChain are not dependencies.

## Data and configuration

Data is stored in **data/app.sqlite3**, with SQLite journal sidecar files as needed. Records survive restart.

To use a new database, stop the app and set DATABASE_PATH to a new filename. To reset, stop the app and rename data to data-backup. Never change database files while the process is running.

Supported environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| HOST | 127.0.0.1 | Bind address |
| PORT | 8083 | HTTP port |
| DATABASE_PATH | data/app.sqlite3 | SQLite file |
| AI_MODE | demo | demo or ollama |
| WORKER_ENABLED | true | Enable SyncBridge worker |
| OLLAMA_BASE_URL | http://127.0.0.1:11434 | Local model endpoint |
| OLLAMA_CHAT_MODEL | llama3.2:3b | Installed chat model |
| OLLAMA_EMBED_MODEL | nomic-embed-text | Installed embedding model |

.env.example is a reference; it is not automatically loaded.

## GenAI behavior

Demo mode is offline keyword retrieval and evidence excerpts, not LLM generation. Optional Ollama mode performs actual embedding and chat calls. See [AI setup](docs/AI_SETUP.md).

## Run tests

With an installed environment:

```powershell
.\.venv\Scripts\python.exe run_tests.py
```

From a project in the Windows-ready suite:

```powershell
..\runtime\python.exe run_tests.py
```

Tests use temporary databases, not your demo data. External model contracts use a mock transport. For the restricted preparation environment, a writable --basetemp under verification-local was supplied; ordinary local runs use pytest's temporary directory.

## Design notes and limitations

PDF, Word, OCR, chat history, streaming and a dedicated vector index are not included. Vectors are stored as JSON arrays and scanned in process. The cosine threshold is fixed at 0.35 and needs evaluation. Keyword overlap can produce weak matches; source labels do not guarantee that every generated statement is correct.

Read [Java to Python mapping](docs/JAVA_TO_PYTHON.md) for transaction and framework differences.

The app binds to loopback by default and is a learning implementation. Production deployment requires real identity management, TLS, an explicit CSRF/origin policy, migrations, monitoring, retention and deployment review. Generated content needs evaluation and human review.

## Extend it

Add PDF extraction with page metadata, pgvector, hybrid retrieval, reranking and a measured evaluation suite.

## Add to GitHub

Suggested repository name: **docquery-ai-python**.

Upload the source, tests, requirements, documentation, samples and workflow. Keep .venv, data, caches and real credentials out of Git. The shared Windows runtime belongs in a release bundle, not a source repository.

Suggested description: **A user-isolated document question-answering service with chunking, retrieval, source excerpts and optional local model generation.**
