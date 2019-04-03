PACKAGE_NAME=iterchain

.PHONY: install dist publish docs lint lint-html tests

install:
	python setup.py install

dist:
	make docs
	python setup.py sdist bdist_wheel

publish:
	make dist
	twine upload dist/*

docs:
	cd docs && make html

lint:
	pylint $(PACKAGE_NAME)

# lint-html:
# 	pylint --output-format=html $(PACKAGE_NAME) > pylint.html

test:
	pytest
	make lint
