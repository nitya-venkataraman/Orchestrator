.DEFAULT_GOAL := help
PY := python3
SKILL := .claude/skills/user-story-generator

.PHONY: help test lint validate run eval clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

test: ## Run the validator self-tests
	$(PY) harness/tests/run_tests.py

lint: ## Structural lint of the skill + eval suite
	$(PY) harness/lint_skill.py

validate: ## Validate a file: make validate FILE=output/delivery/user-stories-2026-09-02.md
	@test -n "$(FILE)" || { echo "usage: make validate FILE=path/to/stories.md"; exit 2; }
	$(PY) harness/validate_stories.py --strict $(FILE)

run: ## Run the skill against every fixture via the local runner (needs `claude` CLI)
	$(PY) harness/run.py $(if $(FIXTURE),--fixture $(FIXTURE),)

eval: ## Run the claude plugin eval suite (needs early access + API key)
	claude plugin eval ./$(SKILL) --eval-dir $(SKILL)/evals $(if $(CASE),--case $(CASE),)

clean: ## Remove generated results and caches
	rm -rf harness/results/*.json harness/results/latest-*.md
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
