#!/bin/bash

echo "Lint check with flake8..."
flake8 yahtzee tests
# flake8 doesn't provide feedback when no issues are found
if [ $? -eq 0 ]; then
	echo "flake8 found no issues."
else
	exit 1
fi

echo "Type check with mypy..."
mypy yahtzee
if [ $? -ne 0 ]; then
	exit 1
fi

echo "Run tests with pytest..."
pytest tests
if [ $? -ne 0 ]; then
	exit 1
fi
