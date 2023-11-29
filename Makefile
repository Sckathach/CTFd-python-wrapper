format:
	black .

pre-commit: format

install_black:
	pip install black
	echo -e '#!/bin/bash\nmake pre-commit' > test

release:
	python setup.py sdist
	cp dist/wrapper* ../CTFdSimulation