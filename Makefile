maint:
	pip install -r requirements/dev.txt
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U setup.py
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

docs:
	python setup.py upload_docs --upload-dir docs/_build/html

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload -s dist/*

test:
	pytest

testall:
	make test
	cheesecake_index -n memtop -v

count:
	cloc . --exclude-dir=docs,cover,dist,memtop.egg-info

countc:
	cloc . --exclude-dir=docs,cover,dist,memtop.egg-info,tests

countt:
	cloc tests

clean:
	rm -f *.hdf5 *.yml *.csv
	rm -rf docs/build
	rm -rf cover
	rm -rf build
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
