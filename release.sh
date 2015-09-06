#!/bin/bash

if echo "$@" | grep -q -- '--version'; then
	VERSION="$(echo "$@" | grep -oh -- '--version=.*' | cut -d '=' -f 2)"
fi

if echo "$@" | grep -q -- '--identity'; then
	IDENTITY="$(echo "$@" | grep -oh -- '--identity=.*' | cut -d '=' -f 2)"
fi
[[ -z "$IDENTITY" ]] && IDENTITY=E80E2315

if [[ -z "$VERSION" ]]; then
	echo "Usage: $(basename $0) --version=VERSION [--identity=IDENTITY]"
	echo " - Current version: $(sed -n "s/__version__ = '\(.*\)'/\1/p" setup.py)"
	exit 1
fi

DATE=$(date +%Y-%m-%d)
sed -i '' "s/__version__ = '.*'/__version__ = '$VERSION'/" setup.py
sed -i '' "s/:Version: .*/:Version: $VERSION of $DATE/" README.rst

git add README.rst setup.sh
git commit -m "version bump"
git push

rm -Rf dist/*
git tag -a v$VERSION -m "pypi version $VERSION"
git push origin v$VERSION
python2.7 setup.py sdist bdist_wheel --universal
twine upload dist/* --sign --identity E80E2315
echo 'done'