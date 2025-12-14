coverage: coverage_run
	@coverage html

coverage_run:
	@coverage run -m pytest test

lint:
	@ruff check triangulator test

test:
	@pytest test

unit_test:
	@pytest test -m "not performance"

perf_test:
	@pytest test -m "performance"

doc:
	@pdoc3 --html triangulator