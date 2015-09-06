#!/bin/bash

if ! git diff-index --quiet HEAD; then
	echo "Can not process, there's uncommited changes."
	exit 1
fi

if echo "$@" | grep -q -- '--version'; then
	VERSION="$(echo "$@" | grep -oh -- '--version=.*' | cut -d '=' -f 2)"
fi

if echo "$@" | grep -q -- '--identity'; then
	IDENTITY="$(echo "$@" | grep -oh -- '--identity=.*' | cut -d '=' -f 2)"
fi
[[ -z "$IDENTITY" ]] && IDENTITY=E80E2315

CURRENT_VERSION=$(sed -n "s/__version__ = '\(.*\)'/\1/p" setup.py)
if [[ -z "$VERSION" ]]; then
	echo "Usage: $(basename $0) --version=VERSION [--identity=IDENTITY]"
	echo " - Current version: $CURRENT_VERSION"
	exit 1
fi

DATE=$(date +%Y-%m-%d)
CHANGELOG=$(mktemp -t tmp)
echo "v$VERSION (${DATE})" > $CHANGELOG
echo "$(git log v${CURRENT_VERSION}..HEAD --oneline | egrep -v "bump|pypi|pep8")" | while read LINE; do
	echo -e "    $LINE" >> $CHANGELOG
done
cat CHANGELOG >> $CHANGELOG
cat $CHANGELOG > CHANGELOG

sed -i '' "s/__version__ = '.*'/__version__ = '$VERSION'/" setup.py
sed -i '' "s/:Version: .*/:Version: $VERSION of $DATE/" README.rst

git add README.rst setup.sh CHANGELOG
git commit -m "version bump and changelog update"
git push

rm -Rf dist/*
git tag -a v$VERSION -m "pypi version $VERSION"
git push origin v$VERSION
python2.7 setup.py sdist bdist_wheel --universal
twine upload dist/* --sign --identity E80E2315
