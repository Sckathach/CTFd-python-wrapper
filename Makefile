VERSION=0.0.0

format:
	black .

doc:
	sphinx-build -b html docs docs/_build

docc:
	rm -rf docs/_build

docx: docc doc
	firefox docs/_build/index.html

pre-commit: format

install_black:
	pip install black
	echo -e '#!/bin/bash\nmake pre-commit' > test

release:
	python -m build
	 git tag -a v0.3.1 -m "Release version 0.3.1"
	 git push --tags
	# cp dist/wrapper* ../CTFdSimulation

test:
	echo "git tag -a v$(VERSION) 'Release version $(VERSION)'"