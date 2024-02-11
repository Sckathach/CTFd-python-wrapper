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
	python setup.py sdist
	cp dist/wrapper* ../CTFdSimulation