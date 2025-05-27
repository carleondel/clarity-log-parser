# Run tests
test:
	pytest tests/

# Export dependencies
freeze:
	pip freeze > requirements.txt

# Install dependencies
install:
	pip install -r requirements.txt

# Run Task 1 CLI
run-task1:
	python main.py data/Optional-connections.log host22 "2024-01-01 00:00:00" "2024-12-30 23:59:59"

# Run Task 2 in batch mode
run-task2:
	python stream.py \
		--logfile data/Optional-connections.log \
		--incoming host22 \
		--outgoing host22 \
		--frequency 31536000 
# 1 year in seconds

# Clean up Python cache
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +; \
	find . -name "*.pyc" -delete