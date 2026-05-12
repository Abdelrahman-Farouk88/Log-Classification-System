Log Classification System
=========================

Classifies log messages using regex, a BERT model, and an LLM fallback for specific sources.
Includes a FastAPI service with a simple web UI for CSV uploads and single-log classification.

Features
--------
- CSV classification with `source` and `log_message` columns
- Single log classification by source
- FastAPI endpoints + UI

Project Structure
-----------------
- [classify.py](classify.py): core classification orchestration
- [server.py](server.py): FastAPI app and endpoints
- [resources/ui.html](resources/ui.html): web UI
- [resources/test.csv](resources/test.csv): sample input
- [resources/output.csv](resources/output.csv): sample output location
- [models/log_classifier.joblib](models/log_classifier.joblib): trained BERT classifier

Requirements
------------
Install dependencies from [requirements.txt](requirements.txt):

```bash
pip install -r requirements.txt
```

If you want to run the API server, install Uvicorn:

```bash
pip install uvicorn
```

Quick Start
-----------
1) Run the classifier on the sample CSV:

```bash
python classify.py
```

2) Start the API server:

```bash
uvicorn server:app --reload
```

3) Open the UI in a browser:

```
http://localhost:8000/
```

API Endpoints
-------------
POST /classify/
	- Upload a CSV file with `source` and `log_message` columns.
	- Returns a labeled CSV file.

POST /classify-text/
	- JSON body: { "source": "...", "log_message": "..." }
	- Returns: { "label": "..." }

Example Request (Single Log)
----------------------------
```bash
curl -X POST http://localhost:8000/classify-text/ \
	-H "Content-Type: application/json" \
	-d "{\"source\":\"LegacyCRM\",\"log_message\":\"Case escalation failed\"}"
```

Notes
-----
- LLM classification uses the Groq client. Configure your API key via environment variables
	in a `.env` file as expected by `python-dotenv`.
- CSV outputs are written to [resources/output.csv](resources/output.csv) by default.
