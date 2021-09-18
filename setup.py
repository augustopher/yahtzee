from setuptools import setup

install_requires = ["tabulate", "simple_term_menu"]
test_requires = ["pytest", "pytest-mock", "pytest-cov"]
docs_requires = ["sphinx", "myst-parser", "sphinx-rtd-theme"]
typecheck_requires = ["mypy", "types-tabulate"]
lint_requires = ["flake8", "interrogate"]
dev_requires = test_requires + docs_requires + typecheck_requires + lint_requires

setup(
    name="yahtzee",
    version="0.0.1",
    packages=["yahtzee"],
    description="CLI game of Yahtzee",
    author="Gus Powers",
    author_email="guspowers0@gmail.com",
    url="https://gitub.com/augustopher/yahtzee",
    license="MIT",
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={
        "test": test_requires,
        "docs": docs_requires,
        "type": typecheck_requires,
        "lint": lint_requires,
        "dev": dev_requires,
    },
)
