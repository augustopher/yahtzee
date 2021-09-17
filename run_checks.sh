#!/bin/bash

usage() {
	echo "usage: ./run_scripts.sh -options"
	echo "-a  Run all checks"
	echo "-l  Run lint check (flake8)"
	echo "-m  Run type check (mypy)"
	echo "-t  Run tests (pytest)"
	echo "-v  Run version check"
	echo "-h  Brings up this message"
}

OPTIND=1

RUN_LINT=0
RUN_TYPE=0
RUN_TEST=0
RUN_VER=0

while getopts "almtvh" opt; do
	case "$opt" in
		a)
			RUN_LINT=1
			RUN_TYPE=1
			RUN_TEST=1
			RUN_VER=1
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
		v)
			RUN_VER=1
			;;
		h)
			usage
			;;
		*)
			usage
			exit 1
			;;
	esac
done

RUN_SOMETHING=$((RUN_LINT + RUN_TYPE + RUN_TEST + RUN_VER))
if [ $RUN_SOMETHING -eq 0 ]; then
	echo "No checks selected, no checks run."
fi

if [ $RUN_VER -gt 0 ]; then
        echo "Checking versions across all files..."
        VER_PATTERN="\d+\.\d+\.\d+([-_][a-zA-z]*)?"
				VER_SETUP=$(grep "version=" setup.py | grep -Eo $VER_PATTERN)
        VER_DOCS=$(grep "release =" docs/conf.py | grep -Eo $VER_PATTERN)
        if [ "$VER_SETUP" != "$VER_DOCS" ]; then
                echo "Versions don't match."
                echo "setup.py at $VER_SETUP, docs/conf.py at $VER_DOCS"
                exit 1
        fi
        echo "All versions match."
fi

if [ $RUN_LINT -gt 0 ]; then
	echo "Lint check with flake8..."
	# flake8 doesn't provide feedback when no issues are found
	if flake8 yahtzee tests; then
		echo "flake8 found no issues."
	else
		exit 1
	fi
fi

if [ $RUN_TYPE -gt 0 ]; then
	echo "Type check with mypy..."
	if ! mypy yahtzee; then
		exit 1
	fi
fi

if [ $RUN_TEST -gt 0 ]; then
	echo "Run tests with pytest..."
	if ! pytest; then
		exit 1
	fi
fi
