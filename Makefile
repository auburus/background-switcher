export PATH := $(HOME)/.local/share/mise/shims:$(PATH)

.PHONY: help
# Show this help
help:
	@echo "Available commands:"
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) \
	| column -s: -t \
	| xargs -I{} printf "  {}\n"

.PHONY: setenv
# Setup dev environment
setenv:
	mise install

.PHONY: format
# Format
format:
	shfmt -w background-switcher scripts/*
	yamlfmt

.PHONY: lint
# Lint
lint:
	shellcheck background-switcher scripts/*
	yamlfmt -lint

.PHONY: run
# Run the program
run:
	$(CURDIR)/background-switcher

.PHONY: install
# Run program on autostart
install:
	@./scripts/install.sh
