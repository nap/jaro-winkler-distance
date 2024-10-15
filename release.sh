#!/usr/bin/env bash
set -e -o pipefail

: "${HATCH_INDEX_REPO:=main}"  # or test

if ! git diff-index --quiet HEAD; then
	echo "Cannot proceed, there are uncommited changes."
	exit 1
fi

if [[ -z "${HATCH_INDEX_USER}" ]] || [[ -z "${HATCH_INDEX_AUTH}" ]]; then
  echo "Make sure environment variables HATCH_INDEX_USER and HATCH_INDEX_AUTH are set."
  exit 1
fi

if echo "$@" | grep -q -- 'help' || [[ ${#@} -lt 1 ]]; then
  echo "Usage: release.sh [help|major|minor|patch]"
  exit 0
fi

if ! echo "$1" | grep -qE "major|minor|patch"; then
  echo "Select one of: major, minor, patch"
  echo "Usage: release.sh [help|major|minor|patch]"
  exit 1
fi

hatch version "$1"

git add ./pyjarowinkler/__about__.py
git commit -m "release version $(hatch version)"
git push
hatch build
# see https://hatch.pypa.io/latest/publish/#authentication
# Set HATCH_INDEX_USER
# Set HATCH_INDEX_AUTH
hatch publish
