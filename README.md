# A Helpful GitHub Actions Workflow


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
help you have a healthier, happier codebase.


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
├── pyproject.toml             # Configuration file for black, interrogate & pytest
├── requirements-dev.txt       # Development requirements file
├── requirements.txt           # Requirements file
├── setup.cfg                  # Configuration file for flake8, mypy
└── tests                      # Test directory for project level tests
    └── projectname
        └── test_example.py
```

- - -

### Installation instructions:

- Copy and paste
  [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) and relevant config files
  into your repo.
- Set a couple of secrets:
  - `CC_TEST_REPORTER_ID` (a repo-specific id provided by Codeclimate)
  See [finding your test coverage token](https://docs.codeclimate.com/docs/finding-your-test-coverage-token).
  - `CODECOV_TOKEN`, a similar token provided by CodeCov. See [where is the repository upload token found](https://docs.codecov.io/docs/frequently-asked-questions#where-is-the-repository-upload-token-found).
  - You don't need to set up `GITHUB_TOKEN` for [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) to work.

- Copy [setup.cfg](setup.cfg) and [pyproject.toml](pyproject.toml) files to the root directory of your repo. These files are being used for configuration of linting, formatting and testing tools invoked by [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml).
- Add `output/` to your top-level `.gitignore`. Things like coverage reports are written to that directory.



  It's a good idea to invoke the configured linting tools locally prior to creating the PR.
  ProTip: it is likely you can configure them in your IDE.
  
Take the workflow for a spin by making a PR in your repo.
  - For black, flake8, mypy you can update the configurations in [setup.cfg](setup.cfg) file, and [pyproject.toml](pyproject.toml) for interrogate, pytest configurations. If you would like to have separate configuration files for each tool, then use them in the workflow file as mentioned below.
  - For black replace the value of `black_args: '--config=pyproject.toml'` in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) under `with` [tag](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L122). This workflow uses default configuration provided by black.
  - For flake8, replace the value of `flake8_args: '--config=setup.cfg'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions#L118)
  - For interrogate, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L161) command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
  - For mypy replace the value of `mypy_flags: '--config-file=setup.cfg'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L130)
  - For pytest, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L138) command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
  - See the FAQ section below or raise an issue if you don't find an answer.

- - -
#### How it works:

- This workflow uses the configuration files for black, flake8, mypy from the [setup.cfg](setup.cfg) and for interrogate and pytest from [pyproject.toml](pyproject.toml) respectively.
- This workflow also creates intermediate output files during the CI build, under `output/` folder, mentioned below:
  - `output/pytest.xml` - contains the test results in junit-xml format - generated by pytest command.[see here](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L142)
  - `output/coverage.xml` - contains the coverage report - generated by coverage.py. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L144)
  - `output/docstring_report.txt` - contains the docstring report - generated by [interrogate](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L159)

#### The checks in the work flow include:
   - Check for empty PR description.
   - Check for unwanted files - `*.zip` etc.
   - Check hardcoded credentials in files.
   - Linting, formatting and type check - black, flake8, interrogate, mypy  
   - Check for missing docstrings using [interrogate](https://github.com/econchick/interrogate)
- Run test suite and generate result & test coverage using codecov; look for code issues with code climate
   
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
- [EnricoMi/publish-unit-test-result-action](https://github.com/EnricoMi/publish-unit-test-result-action) - for unit test result comment.

- - -

## FAQ

**Question:** What's `GITHUB_TOKEN` and do I need to set it up to run [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)?

**Answer:** No. GitHub automatically creates a GITHUB_TOKEN secret to use in your workflow. You can use the `GITHUB_TOKEN` to authenticate in a workflow run.
When you enable GitHub Actions, GitHub installs a GitHub App on your repository. The`GITHUB_TOKEN` secret is a GitHub App installation access token. You can use the installation access token to authenticate on behalf of the GitHub App installed on your repository. The token's permissions are limited to the repository that contains your workflow. Before each job begins, GitHub fetches an installation access token for the job. The token expires when the job is finished.
You can read more about this [here](https://docs.github.com/en/actions/reference/authentication-in-a-workflow)

##

**Question:** How can I add secrets to repo and test them in workflow?

**Answer:** Secrets are encrypted environment variables that you create in an organization, repository, or repository environment. The secrets that you create are available to use in GitHub Actions workflows. You can read more about how to setup secrets in the repo [here](https://docs.github.com/en/actions/reference/encrypted-secrets)
To use the secret in your workflow file you can simply use an expression: `${{ secrets.YOUR_SECRET_NAME }}` to evaluate your secret in workflow steps.

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

 In our case, `workflows: ["PM CI Workflow"]` -  "CI Workflow" is the workflow [name](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L8) of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)

##

**Question:** How does hardcoded secrets scan work in the workflow?

**Answer:** The workflow uses [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) action to detect the secrets in code.
 [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) action uses [detect-secrets](https://github.com/Yelp/detect-secrets) which is a module for detecting secrets within a code base. \
 For tweaking the behaviour of secret scan for the workflow run, you can change the configuration of [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) in [pm-gh-actions.yml](https://github.com/predictionmachine/pm-gh-actions/blob/38f69ab7f32a385b251838e81b85449327e04f83/.github/workflows/pm-gh-actions.yml#L92). \
 For more details please see [reviewdog/action-detect-secrets](https://github.com/reviewdog/action-detect-secrets) and [detect-secrets](https://github.com/Yelp/detect-secrets)

- - -
Developed and used by _Prediction Machine_.

