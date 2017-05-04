test:
	@pytest -v test

docs:
	@sphinx-apidoc -f -o docs oriole_service
	@sphinx-build docs docs/build/html

.PHONY: test docs
