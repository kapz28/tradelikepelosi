# TradeLikePelosi

[![Release](https://img.shields.io/github/v/release/kapz28/TradeLikePelosi)](https://img.shields.io/github/v/release/kapz28/TradeLikePelosi)
[![Build status](https://img.shields.io/github/actions/workflow/status/kapz28/TradeLikePelosi/main.yml?branch=main)](https://github.com/kapz28/TradeLikePelosi/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/kapz28/TradeLikePelosi/branch/main/graph/badge.svg)](https://codecov.io/gh/kapz28/TradeLikePelosi)
[![Commit activity](https://img.shields.io/github/commit-activity/m/kapz28/TradeLikePelosi)](https://img.shields.io/github/commit-activity/m/kapz28/TradeLikePelosi)
[![License](https://img.shields.io/github/license/kapz28/TradeLikePelosi)](https://img.shields.io/github/license/kapz28/TradeLikePelosi)

This is a python HFT trading bot that analyzes american politicians insider trading and pulls trades on wealthsimple

- **Github repository**: <https://github.com/kapz28/TradeLikePelosi/>
- **Documentation** <https://kapz28.github.io/TradeLikePelosi/>

## Getting started with your project

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:kapz28/TradeLikePelosi.git
git push -u origin main
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

## Releasing a new version

- Create an API Token on [Pypi](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/kapz28/TradeLikePelosi/settings/secrets/actions/new).
- Create a [new release](https://github.com/kapz28/TradeLikePelosi/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
