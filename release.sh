#!/usr/bin/env bash
set -e -o pipefail

: "${PYPI_REPO:=test}" # or main
: "${USAGE_HELP:="Usage: release.sh [help|major|minor|patch]"}"

if echo "$@" | grep -q -- 'help' || [[ ${#@} -lt 1 ]]; then
  echo "${USAGE_HELP}"
  exit 0
fi

if ! git diff-index --quiet HEAD; then
  echo "Cannot proceed, there are uncommited changes."
  echo "${USAGE_HELP}"
  exit 1
fi

if ! echo "$1" | grep -qE "major|minor|patch"; then
  echo "Select one of: major, minor, patch"
  echo "${USAGE_HELP}"
  exit 1
fi

export PYPI_REPO_USER="PYPI_${PYPI_REPO^^}_USER"
export PYPI_REPO_AUTH="PYPI_${PYPI_REPO^^}_AUTH"
if [[ ! -v "${PYPI_REPO_USER}" || ! -v "${PYPI_REPO_AUTH}" ]]; then
  echo "You must set environment variable ${PYPI_REPO_USER} and ${PYPI_REPO_AUTH}"
  echo "${USAGE_HELP}"
  exit 1
fi

hatch version "${1}"

if [[ "${PYPI_REPO}" == "main" ]]; then
  git add ./pyjarowinkler/__about__.py
  git commit -m "release version $(hatch --no-color version | tr -d '\n')"
  git push
fi

hatch build --clean
hatch publish \
  --repo "${PYPI_REPO}" \
  --user "${!PYPI_REPO_USER}" \
  --auth "${!PYPI_REPO_AUTH}"

echo "done."