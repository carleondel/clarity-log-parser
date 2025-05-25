# Run tests
test:
	pytest tests/

# Export dependencies
freeze:
	pip freeze > requirements.txt

# Install dependencies
install:
	pip install -r requirements.txt

# Run the CLI tool (adjust arguments as needed)
run:
	python main.py data/Optional-connections.log host22 "2024-01-01 00:00:00" "2024-12-30 23:59:59"