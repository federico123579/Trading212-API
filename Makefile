version = 'v0.1b5'

clean:
	@find . -name "*.pyc" -delete

dependencies:
	@pip install .

dev-dependencies:
	@pip install -e .
	@pip install -r dev-requirements.txt

release:
	@sed -ic -e s/`cat VERSION`/$(version)/ setup.py tradingAPI/__init__.py
	@make clean
	@echo $(version) > VERSION
	@git add setup.py VERSION tradingAPI/__init__.py
	@git commit -m "setup: bump to $(version)"
	@git tag $(version)
	@git push --tags
	@git push
	@python setup.py sdist bdist_wheel upload
