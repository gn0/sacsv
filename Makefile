VERSION = $(shell grep '^version = "' pyproject.toml | cut -d'"' -f2)

TARGETS := dist/sacsv-$(VERSION)-py3-none-any.whl
TARGETS += dist/sacsv-$(VERSION).tar.gz

.PHONY: build
build: $(TARGETS)

dist/sacsv-%-py3-none-any.whl:
	uv build --wheel .

dist/sacsv-%.tar.gz:
	uv build --sdist .

.PHONY: test
test:
	uv run pytest -v --cov=src

.PHONY: upload
upload: $(TARGETS)
	uv publish $^

.PHONY: clean
clean:
	-rm -rf dist/
