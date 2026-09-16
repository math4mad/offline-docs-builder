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
    git clone --depth 1 --branch "v${VERSION}" "https://github.com/${REPO}.git" "$work_dir/src"
    cd "$work_dir/src/doc"
    pip install -r requirements.txt
    make html
    cp -R _build/html/. "$OLDPWD/resources/"
    ;;
  *)
    echo "Unknown strategy: $STRATEGY" >&2
    exit 1
esac