# System Architecture

## Architectural style

The Lab 8 prototype uses a browser-server design. A single Python process serves the UI and HTTP API and uses SQLite for persistence. This lets the group demonstrate the triage workflow with one application process and one Docker image.

## Component interaction

~~~mermaid
flowchart TD
    Reviewer[Reviewer] --> UI[Browser form]
    UI --> API[HTTP service]
    API --> Rules[Recommendation logic]
    API <--> DB[(SQLite)]
    API --> Result[Recommendation for review]
~~~

## Data flow

1. The reviewer enters a synthetic bug report. The browser submits the title and description as JSON.
2. The HTTP handler validates both fields and reads up to 100 recent titles. The recommendation logic applies keyword rules and compares title-token overlap.
3. The app stores the ticket and suggestions in SQLite, then displays the result in the browser for human review.

## ADR 01 — Use local rules and SQLite for the lab prototype

The prototype needed a repeatable demonstration without credentials or external services. A small rule set and SQLite support that setup. Keyword matching can miss synonyms and context, and the database is intended for a single local demonstration. Model-based recommendations and issue-tracker integration remain future work from the project proposal.
