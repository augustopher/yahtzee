#!/bin/bash

OPTIND=1

RUN_LINT=0
RUN_TYPE=0
RUN_TEST=0

while getopts "almt" opt; do
  case "$opt" in
    a)
      RUN_LINT=1
      RUN_TYPE=1
      RUN_TEST=1
      ;;
    l)
      RUN_LINT=1
      ;;
    m)
      RUN_TYPE=1
      ;;
    t)
      RUN_TEST=1
      ;;
  esac
done

if [ $RUN_LINT -gt 0 ]; then
	echo "Lint check with flake8..."
	flake8 yahtzee tests
	# flake8 doesn't provide feedback when no issues are found
	if [ $? -eq 0 ]; then
		echo "flake8 found no issues."
	else
		exit 1
	fi
fi

if [ $RUN_TYPE -gt 0 ]; then
	echo "Type check with mypy..."
	mypy yahtzee
	if [ $? -ne 0 ]; then
		exit 1
	fi
fi

if [ $RUN_TEST -gt 0 ]; then
	echo "Run tests with pytest..."
	pytest tests
	if [ $? -ne 0 ]; then
		exit 1
	fi
fi