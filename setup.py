from setuptools import setup

install_requires = ["tabulate"]
test_requires = ["pytest", "pytest-mock", "pytest-cov"]
docs_requires = ["sphinx", "myst-parser", "sphinx-rtd-theme"]
typecheck_requires = ["mypy", "types-tabulate"]
lint_requires = ["flake8"]

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
        "test": install_requires + test_requires,
        "docs": install_requires + docs_requires,
        "type": install_requires + typecheck_requires,
        "lint": install_requires + lint_requires,
        "dev": install_requires + test_requires + docs_requires + typecheck_requires + lint_requires,
    },
)
