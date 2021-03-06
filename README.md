# A Helpful GitHub Actions Workflow
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![PM CI workflow](https://github.com/predictionmachine/pm-coding-template/actions/workflows/pm-gh-actions.yml/badge.svg)](https://github.com/predictionmachine/pm-coding-template/actions/workflows/pm-gh-actions.yml)
[![codecov](https://codecov.io/gh/predictionmachine/pm-github-actions/branch/main/graph/badge.svg?token=2AQW1NP110)](https://codecov.io/gh/predictionmachine/pm-github-actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/47ce8331f863c98ca216/maintainability)](https://codeclimate.com/github/predictionmachine/pm-github-actions/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<!-- see https://app.codecov.io/gh/predictionmachine/pm-github-actions/settings/badge -->
<!-- see https://codeclimate.com/github/predictionmachine/pm-github-actions/badges#maintainability-markdown -->

This repository provides a **GitHub Actions [workflow](.github/workflows/pm-gh-actions.yml)** to check and nicely comment on
pull requests in python code bases.

It will help with:
- _PR quality_, like making sure there _is_ a description and there aren't secrets or .zip and similar files
  being checked in
- _Code quality_, by running tools like
  - `black` for consistent formatting,
  - `flake8` for pip8 conformance,
  - `interrogate` for presence of docstrings,
  - `mypy` for typechecking,
  - `pytest` for testing.

It also reports to [codecov](https://about.codecov.io/) and
[codeclimate quality](https://codeclimate.com/quality/) to
help you have a healthier, easier to evolve codebase.


 - - -

### Folder structure convention
Getting these tools and checks to work together nicely takes some configuration.
The expected layout is:

```bash
.
├── .github
│   └── workflows              # Workflow directory for your workflow files
│       └── pm-gh-actions.yml
├── projectname                # Project directory - top level directory for project
│   └── example.py
├── .codeclimate.yml           # Configuration file for codeclimate analysis
├── .pre-commit-config.yaml    # pre-commit configuration file, see https://pre-commit.com
├── pyproject.toml             # Configuration file for black, interrogate, mypy & pytest
├── requirements-dev.txt       # Development requirements file
├── requirements.txt           # Requirements file
├── setup.cfg                  # Configuration file for flake8, mypy
└── tests                      # Test directory for project level tests
    └── projectname
        └── test_example.py
```

- - -

## Installation:

- Copy and paste
  [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) and relevant config files. OR call this workflow as one of the jobs under your repo's workflow - this workflow is [reusable workflow](https://docs.github.com/en/actions/learn-github-actions/reusing-workflows), so you can call this from your workflow as followed:

  ```YAML
  # file: caller_workflow_name.yaml

  name: CI workflow
  on:
    push:
      branches:
        - main
    pull_request:
      types:
        - opened
      branches:
        - main

  jobs:
    # reference: https://docs.github.com/en/actions/learn-github-actions/reusing-workflows#example-caller-workflow
    org-checks:
      uses: predictionmachine/pm-github-actions/.github/workflows/pm-gh-actions.yml@main
      secrets:
        CC_TEST_REPORTER_ID: ${{ secrets.CC_TEST_REPORTER_ID }}
        CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
  ```

- Set a couple of secrets:
  - `CC_TEST_REPORTER_ID` (a repo-specific id provided by Codeclimate)
  See [finding your test coverage token](https://docs.codeclimate.com/docs/finding-your-test-coverage-token).
  - `CODECOV_TOKEN`, a similar token provided by CodeCov. See [where is the repository upload token found](https://docs.codecov.io/docs/frequently-asked-questions#where-is-the-repository-upload-token-found).
  - You don't need to set up `GITHUB_TOKEN` for [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) to work.

- Copy [setup.cfg](setup.cfg), [pyproject.toml](pyproject.toml) and [.codeclimate.yml](.codeclimate.yml) files to the root directory of your repo. These files are being used for configuration of linting, formatting, testing and code analysis (using [code climate](https://docs.codeclimate.com/)) tools invoked by [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml).
- Add `output/` to your top-level `.gitignore`. Things like coverage reports are written to that directory.


  It's a good idea to invoke the configured linting tools locally prior to creating the PR.
  ProTip: it is likely you can configure them in your IDE.

  You can also configure and use [pre-commit hooks](https://pre-commit.com/#plugins). \
  Copy [.pre-commit-config.yaml](.pre-commit-config.yaml) to the root directory of your repo and follow the [installation](https://pre-commit.com/#installation) instructions to run it.

Take the workflow for a spin by making a PR in your repo.
  - `black` and `flake8` configurations are in [setup.cfg](setup.cfg); `interrogate`, `mypy` and `pytest` are in [pyproject.toml](pyproject.toml); code climate configurations are in [.codeclimate.yml](.codeclimate.yml), update as needed.
  - **UPDATE** in [pyproject.toml](pyproject.toml), added `[tool.mypy]` and `[[tool.mypy.overrides]]` section.
  - For more config tips see the FAQ below or raise an issue labeled "question".

- - -
### How it works:

- This workflow uses the configuration files for black and flake8 from the [setup.cfg](setup.cfg); interrogate, mypy and pytest from [pyproject.toml](pyproject.toml) and for code analysis from [.codeclimate.yml](.codeclimate.yml) respectively.
- This workflow also creates intermediate output files during the CI build, under `output/` folder, mentioned below:
  - `output/coverage.xml` - contains the coverage report - generated by coverage.py.
  - `output/docstring_report.txt` - contains the docstring report - generated by interrogate.

#### The checks in the work flow include:
   - Check for valid branch name as per [pm-coding-template](https://github.com/predictionmachine/pm-coding-template#github-branches-pull-requests) standard.
   - Check for empty PR description.
   - Check for unwanted files - `*.zip` etc.
   - Check hardcoded credentials in files.
   - Linting, formatting and type check - black, flake8, interrogate, mypy
   - Check for missing docstrings using [interrogate](https://github.com/econchick/interrogate)
   - Run test suite & coverage using codecov; look for code issues with code climate

**Note**: For the above checks, the `github-actions` bot will comment on the issues in the PR and fail the relevant check if it finds problems.

- - -

### Few screenshots from the PR:

- Empty PR description check:
![empty-pr](docs/screenshots/empty-pr-comment.png?raw=true "Empty PR comment")
- Black format check:
![Alt text](docs/screenshots/black-report.png?raw=true "Black format")
- flake8 checks
![Alt text](docs/screenshots/flake8-report.png?raw=true "Flake8")
- Hardcoded secret check:
![Alt text](docs/screenshots/secrets_report.png?raw=true "Hardcoded secrets report")

**(see more screenshots [here](/docs/screenshots))**

#### The GH action from marketplace used are:

- [reviewdog](https://github.com/reviewdog) - for black, flake8, hard code credentials and mypy
- [sticky-pull-request-comment](https://github.com/marocchino/sticky-pull-request-comment) - for PR comments.
- [paambaati/codeclimate-action](https://github.com/paambaati/codeclimate-action) - for code climate test coverage comments.

- - -

## FAQ

**Question:** What's `GITHUB_TOKEN` and do I need to set it up to run [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)?

**Answer:** No. GitHub automatically creates a GITHUB_TOKEN secret to use in your workflow. You can use the `GITHUB_TOKEN` to authenticate in a workflow run.
When you enable GitHub Actions, GitHub installs a GitHub App on your repository. The`GITHUB_TOKEN` secret is a GitHub App installation access token. You can use the installation access token to authenticate on behalf of the GitHub App installed on your repository. The token's permissions are limited to the repository that contains your workflow. Before each job begins, GitHub fetches an installation access token for the job. The token expires when the job is finished.
You can read more about this [here](https://docs.github.com/en/actions/reference/authentication-in-a-workflow)

##

**Question:** How can I add secrets to repo and test them in workflow?

**Answer:** Yep. Secrets are encrypted environment variables that you create in an organization, repository, or repository environment.
To use the secret, simply use an expression: `${{ secrets.YOUR_SECRET_NAME }}` in a workflow step.
You can read more about how to [setup secrets](https://docs.github.com/en/actions/reference/encrypted-secrets)

##

**Question:** How do I tweak configurations of the checkers?

**Answer:**
If you want to pass additional args, change location of config file, proceed as follows:

 - For black replace the value of `black_args: '--config=pyproject.toml'` in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml). This workflow uses default configuration provided by black.
  - For flake8, replace the value of `flake8_args: '--config=setup.cfg'` to your config file present in the repo.
  - For interrogate, you need to add configuration file path to `interrogate` command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
  - For mypy replace the value of `mypy_flags: '--config-file=setup.cfg'` to your config file present in the repo.
  - For pytest, you need to add configuration file path to `pytest` command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
  - For code climate, you need to update configurations in [.codeclimate.yml](.codeclimate.yml) file.

##

**Question:** How can I execute an additional workflow after this workflow succeeds?

**Answer:** If you want to make a conditional run (stage-wise/sequential) for your existing workflow after successful execution of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) workflow then include following yml code in your existing workflow file on top:

    ```yaml
    on:
     workflow_run:
          workflows: ["PM CI Workflow"] # name of the workflow you want to execute after
          types:
            - completed
    ```

 In our case, `workflows: ["PM CI Workflow"]` -  "CI Workflow" is the workflow `name` of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)

##

**Question:** How does hardcoded secrets scan work in the workflow?

**Answer:** The workflow uses [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) action to detect the secrets in code.
 [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) action uses [detect-secrets](https://github.com/Yelp/detect-secrets) which is a module for detecting secrets within a code base. \
 For tweaking the behaviour of secret scan for the workflow run, you can change the configuration of [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml). \
 For more details please see [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) and [detect-secrets](https://github.com/Yelp/detect-secrets)

- - -

Developed and used by [Prediction Machine](https://predmachine.com/).
