# Offline Docs Builder

Build offline documentation bundles for Python libraries and package them as
Neutralino applications for macOS, Windows, and Linux.

## Prerequisites

- Python 3.10+
- `PyYAML` and `requests`
- `curl`, `unzip`, and `git`
- Node.js and the Neutralino CLI (`npm install --global @neutralinojs/neu`)

Install the Python dependencies with:

```sh
python3 -m pip install -r requirements.txt
```

## Workflow

List configured libraries:

```sh
python3 scripts/list-libraries.py
python3 scripts/get_strategy.py NumPy
```

Fetch documentation into `resources/`. The download script takes the library
metadata explicitly so it can also be used from CI:

```sh
scripts/download-docs.sh NumPy 2.3.3 direct_download numpy/numpy https://numpy.org/doc/
```

Build a Neutralino application from those resources:

```sh
python3 scripts/build_neutralino.py numpy 2.3.3 resources artifacts
```

The generated application is placed in `artifacts/`. Release automation can
then group platform artifacts with `scripts/create-releases.py`; it requires
the GitHub CLI (`gh`) authenticated to the target repository.

## Configuration

- `libraries.yaml` contains library metadata and download strategies.
- `neutralino.config.json` defines the desktop application defaults.
- `templates/index.html` is the fallback document entry page.
