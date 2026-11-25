# Development Methodology

## Software development lifecycle

Use iterative development. The term project plan starts with requirements and design, followed by core platform development, triage development, integration, testing, and deployment. The Lab 8 increment demonstrates one workflow from bug intake through human review. Use GitHub Issues with acceptance criteria to track work.

## Version control and branching

Use GitHub Flow. Keep main runnable and create short-lived feature, fix, or docs branches for individual changes. Use descriptive commit messages such as Docs: add initial README. Open pull requests against main and link the related issue when applicable.

## Code review and definition of done

1. A teammate reviews the diff and confirms that only project files and synthetic examples are included.
2. The prototype starts and responds to its health check.
3. A valid report returns all recommendation fields. A repeated report produces a duplicate suggestion, and malformed input is rejected.
4. README instructions and any affected technical documentation are current before merge.

## Testing and quality assurance

Exercise the rule logic with synthetic examples for each category and severity. Submit a report through the HTTP API, try invalid input, and submit the same title twice to verify SQLite-backed duplicate detection. For release verification, build and run the image, check the form and API, and repeat the same test after pulling the published image.
