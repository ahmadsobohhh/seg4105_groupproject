# AI Software Bug Triage Platform

SEG4105 Lab 8 prototype. Submit a synthetic bug report and review the suggested category, severity, team, summary, and possible duplicate. Suggestions use deterministic rules. The reviewer makes the triage decision.

## Run on Windows

~~~bat
python app.py
~~~

Open http://localhost:8080. Python 3.12 is sufficient and no external packages are required.

Try the title **Login timeout** and the description **The login session hits a timeout when users sign in.** The recommendation should be Authentication, High, and Identity. Submit the same report again to see the possible duplicate.

## Run with Docker

~~~bat
docker build -t seg4105-bug-triage:1.0 .
docker run --rm -p 127.0.0.1:8080:8080 seg4105-bug-triage:1.0
~~~

The app uses SQLite in the local data folder. The example container uses temporary storage that is removed when the container exits. Use synthetic reports for the lab demo.

## Documentation

- [Software components](docs/COMPONENTS.md)
- [System architecture](docs/ARCHITECTURE.md)
- [Development methodology](docs/METHODOLOGY.md)
