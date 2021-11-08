#!/bin/bash

REPO_DIR="$PWD"
PKG_DIR="$REPO_DIR/yahtzee"
TEST_DIR="$REPO_DIR/tests"
DOC_DIR="$REPO_DIR/docs"

usage() {
    echo "usage: ./run_scripts.sh -options"
    echo "-a  Run all checks"
    echo "-l  Run lint check (flake8, interrogate)"
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
            exit 0
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
    VER_SETUP=$(grep "version=" "$REPO_DIR"/setup.py | grep -Eo "$VER_PATTERN")
    VER_DOCS=$(grep "release =" "$DOC_DIR"/conf.py | grep -Eo "$VER_PATTERN")

    if [ "$VER_SETUP" != "$VER_DOCS" ]; then
        echo "Versions don't match."
        echo "$REPO_DIR/setup.py at $VER_SETUP"
        echo "$DOC_DIR/conf.py at $VER_DOCS"
        exit 1
    fi

    echo "All versions match."
fi

if [ $RUN_LINT -gt 0 ]; then
    echo "Lint check with flake8..."
    if ! flake8 "$PKG_DIR"; then
        exit 1
    fi
    if ! flake8 --ignore=D "$TEST_DIR"; then
        exit 1
    fi
    # flake8 doesn't provide feedback when no issues are found
    echo "flake8 found no issues."

    echo "Docstring check with interrogate..."
    if ! interrogate "$PKG_DIR"; then
        exit 1
    fi
fi

if [ $RUN_TYPE -gt 0 ]; then
    echo "Type check with mypy..."
    if ! mypy "$PKG_DIR"; then
        exit 1
    fi
fi

if [ $RUN_TEST -gt 0 ]; then
    echo "Run tests with pytest..."
    if ! pytest "$TEST_DIR"; then
        exit 1
    fi
fi
