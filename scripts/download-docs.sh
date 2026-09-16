#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 5 ]]; then
  echo "Usage: $0 LIBRARY VERSION STRATEGY REPO DOC_URL" >&2
  exit 2
fi

LIBRARY=$1
VERSION=$2
STRATEGY=$3
REPO=$4
DOC_URL=$5

mkdir -p resources
work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT
archive="$work_dir/docs.zip"

case $STRATEGY in
  github_release)
    curl --fail --location "https://github.com/${REPO}/releases/download/v${VERSION}/${LIBRARY}-${VERSION}-doc.zip" -o "$archive"
    unzip -o "$archive" -d resources/
    ;;
  direct_download)
    curl --fail --location "${DOC_URL}${VERSION}/archive.zip" -o "$archive"
    unzip -o "$archive" -d resources/
    ;;
  sphinx_build)
    if ! git clone --depth 1 --branch "v${VERSION}" "https://github.com/${REPO}.git" "$work_dir/src"; then
      rm -rf "$work_dir/src"
      git clone --depth 1 --branch "${VERSION}" "https://github.com/${REPO}.git" "$work_dir/src"
    fi
    python - "$work_dir/src/doc/ext/docscrape.py" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
source = source.replace("except TypeError:\n                signature", "except (TypeError, ValueError):\n                signature")
path.write_text(source, encoding="utf-8")
PY
    sed -i '' 's/SPHINXOPTS += -W --keep-going/SPHINXOPTS += --keep-going/' "$work_dir/src/doc/Makefile"
    cd "$work_dir/src/doc"
    pip install -r requirements.txt
    if ! make html; then
      if [[ ! -f _build/html/index.html ]]; then
        echo "Documentation build failed without usable HTML output." >&2
        exit 1
      fi
      echo "Documentation build reported errors; packaging the generated HTML." >&2
    fi
    cp -R _build/html/. "$OLDPWD/resources/"
    ;;
  *)
    echo "Unknown strategy: $STRATEGY" >&2
    exit 1
esac