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

CURRENT_VERSION=$(hatch version)
echo "Current version: {$CURRENT_VERSION}"

hatch version "$1" > /dev/null 2>&1
FUTURE_VERSION=$(hatch version)
echo "Current version: ${FUTURE_VERSION}"

DATE=$(date +%Y-%m-%d)
CHANGELOG=$(mktemp -t tmp)
echo "v{$CURRENT_VERSION}  (${DATE}) - $(git config --get user.name) <$(git config --get user.email)>" > "${CHANGELOG}"
while read -r LINE; do
	echo -e "    ${LINE}" >> "${CHANGELOG}"
done <<< "$(git log "v${CURRENT_VERSION}..HEAD" --pretty='format:%h %s by %cn on %as' -- ':*.py')"
cat ./CHANGELOG >> "${CHANGELOG}"
cat "${CHANGELOG}" > ./CHANGELOG

git add ./pyjarowinkler/__about__.py ./CHANGELOG
git commit -m "version bump and changelog update"
git push
hatch build
# see https://hatch.pypa.io/latest/publish/#authentication
# Set HATCH_INDEX_USER
# Set HATCH_INDEX_AUTH
hatch publish
