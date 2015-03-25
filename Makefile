docs:
	python setup.py upload_docs --upload-dir docs/_build/html

update:
	python setup.py sdist upload --sign
	sudo pip install memtop --upgrade

test:
	nosetests --with-coverage --cover-erase --cover-package memtop --logging-level=INFO --cover-html

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
	rm *.hdf5 *.yml *.csv