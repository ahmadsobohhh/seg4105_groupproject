# Software Components

| Component | Path | Responsibility | Dependencies |
| --- | --- | --- | --- |
| Browser form and results | index.html | Collect the title and description, show recommendations, and report validation errors | Browser, DOM, Fetch API |
| HTTP handler | app.py | Serve the form and health check, validate input, and return a JSON recommendation | Python standard library |
| Recommendation logic | app.py | Assign category, severity, and suggested team, shorten the description, and identify similar titles | Keyword rules, regular expressions |
| Local database | app.py, data/triage.sqlite3 | Save submissions and recommendations and supply earlier titles for comparison | SQLite |
| Container | Dockerfile | Package and start the local web server on port 8080 | Python 3.12 slim Linux image |

## External interfaces

- GET / returns the browser form. GET /health returns a JSON health response.
- POST /api/reports accepts JSON with title and description. It returns the report ID, category, severity, suggested team, summary, and possible duplicate.
- The application writes reports and their recommendations to SQLite. The reviewer decides how to route the report.
