.PHONY: test install clean

test:
	PYTHONPATH=. python3 -m pytest tests/

install:
	pip install -e .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf *.egg-info .pytest_cache
