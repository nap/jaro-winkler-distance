#!/usr/bin/env bash
set -e -o pipefail

: "${PYPI_REPO:=test}" # or main
: "${USAGE_HELP:="Usage: release.sh [help|major|minor|patch]"}"

if echo "$@" | grep -q -- 'help' || [[ ${#@} -lt 1 ]]; then
  echo "${USAGE_HELP}"
  exit 0
fi

stubgen --package pyjarowinkler --output .

if ! git diff --quiet HEAD -- . ':(exclude)release.sh' ':(exclude)uv.lock'; then
  echo "Cannot proceed, there are uncommitted changes."
  echo "${USAGE_HELP}"
  exit 1
fi

if ! echo "$1" | grep -qE "major|minor|patch"; then
  echo "Select one of: major, minor, patch"
  echo "${USAGE_HELP}"
  exit 1
fi

! gh auth status >/dev/null && exit 1

export PYPI_REPO_USER="PYPI_${PYPI_REPO^^}_USER"
export PYPI_REPO_AUTH="PYPI_${PYPI_REPO^^}_AUTH"
if [[ -z "${!PYPI_REPO_USER}" || -z "${!PYPI_REPO_AUTH}" ]]; then
  echo "You must set environment variable ${PYPI_REPO_USER} and ${PYPI_REPO_AUTH}"
  echo "${USAGE_HELP}"
  exit 1
fi

export VERSION=$(uv version --short --bump "${1}")

if [[ "${PYPI_REPO}" == "main" ]]; then
  git add pyproject.toml uv.lock
  git commit -m "release version ${VERSION}"
  git push
  git tag -sa "v${VERSION}" -m "pypi version release v${VERSION}"
  git push origin "v${VERSION}"
  gh release create "v${VERSION}" ./dist/* --generate-notes
fi

[[ -d ./dist ]] && rm -vRf ./dist

uv build
uv publish --token "${!PYPI_REPO_AUTH}"

echo "Done publishing ${VERSION}."