#!/bin/bash

VERSION=$1
if [[ -z "$VERSION" ]]; then
	echo "First parameter is empty, set version number"
	echo "Current version is set to: $(sed -n "s/__version__ = '\(.*\)'/\1/p" setup.py)"
	exit 1
fi

DATE=$(date +%Y-%m-%d)
sed -i -e "s/__version__ = '.*'/__version__ = '$VERSION'/" setup.py
sed -i -e "s/:Version: .*/:Version: $VERSION of $DATE/" README.rst

git add README.rst setup.sh
git commit -m "version bump"
git push

git tag -a v$VERSION -m "pypi version $VERSION"
git push origin v$VERSION
python2.7 setup.py sdist bdist_wheel --universal
twine upload dist/* --sign --identity E80E2315
