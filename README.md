# pm-gh-actions

Repository for sanity checking and nicely commenting on pull requests for python repositories.
Provides a GitHub Actions workflow file which you can customize. By default, assumes you are a fan of
`black` (for layout), `flake8` for further pip8 conformance, `mypy` for typechecking, and `pytest` and _codeclimate quality_ for testing and coverage.
Developed and used by _Prediction Machine_.

 - - -

## [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)

> ### Folder structure convention

```bash
.
├── .github
│   └── workflows              # Workflow directory for your workflow files
│       └── pm-gh-actions.yml
├── LICENSE
├── README.md
├── docs                       # Documentation directory (alternatively `doc`)
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

- The [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) expects above folder structure for your codebase to follow for a successful run of workflow.
- Change in folder structure requires changes in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) as well, because commands in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) are based on above folder structure.
- The  `main` branch will have a latest [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml). You can always refer to `main` branch to see latest changes of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)

- - -

### Installation instructions:

- To use [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) in your project repo, copy [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) from this repo, and paste it in the `.github/workflows/` folder of your project repo.
- Once you have copied the [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) to `.github/workflows/` folder, set the value of `CC_TEST_REPORTER_ID` in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml). The value is used for reporting the test coverage to code climate, to your repo specific reporter id. See [finding your test coverage token](https://docs.codeclimate.com/docs/finding-your-test-coverage-token) for obtaining the id.
- Next step is to copy [setup.cfg](setup.cfg) and [pyproject.toml](pyproject.toml) file to the root directory of your repo. These files are being used for configuration of linting, formatting and testing tools invoked by [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml). You can also invoke these tools locally prior to creating the PR.
- Once the above steps are done you can run the workflow and test. You don't need to set up any other secrets like `GITHUB_TOKEN` for [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) to work.
- For coverage run, this workflow assumes `tests` folder to be present in the repo else it will fail. If you want to add a different folder for coverage then you need to edit this `coverage run --source=tests -m pytest` [command](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.ym#L139) in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml), replacing `tests` with your location of tests.
  - If you need [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) to use different configurations or configuration files for black, flake8, mypy, interrogate and pytest, then you can define them in the workflow file as below.
  - For black, flake8, mypy you can update the configurations in [setup.cfg](setup.cfg) file, and [pyproject.toml](pyproject.toml) for interrogate, pytest configurations. If you would like to have separate configuration files for each tool, then use them in the workflow file as mentioned below.
  - For black replace the value of `black_args: '--config=pyproject.toml'` in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) under `with` [tag](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L122). This workflow uses default configuration provided by black.
  - For flake8, replace the value of `flake8_args: '--config=setup.cfg'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions#L118)
  - For mypy replace the value of `mypy_flags: '--config-file=setup.cfg'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L130)
  - For interrogate, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L161) command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
  - For pytest, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L138) command in [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) file.
- Please see FAQ section if you have any questions, feel free to raise an issue if you don't find an answer to your question.

**Note:**

- If you are running the commands mentioned in the workflow file locally, then please add `output/` to your `.gitignore` file [see here](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.gitignore#L10), as this folder contains intermediate output files generated in CI build. [know more](#How-it-works)

- - -
#### How it works:

- Run the checks (as mentioned in the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template)) as a CI build process (it can be used in other repo's)
- This workflow uses the configuration files for black, flake8, mypy from the [setup.cfg](setup.cfg) and for pytest and interrogate from [pyproject.toml](pyproject.toml) respectively.
- This workflow also creates an intermediate output files during the CI build, under `output/` folder, mentioned below:
  - `pytest.xml` - contains the test results in junit-xml format - generated by pytest command.[see here](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L142)
  - `coverage.xml` - contains the coverage report - generated by coverage.py. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L144)
  - `docstring_report.txt` - contains the docstring report - generated by [interrogate](https://github.com/predictionmachine/pm-gh-actions/blob/63bc3b28a6c48be33ad01c91cc14ad301cc7ec9a/.github/workflows/pm-gh-actions.yml#L159)

#### The check included in the CI build for workflow file is:
   - Check for empty PR description.
   - Check for unwanted files - .zip etc.
   - Check hardcoded credentials in files.
   - Linting, formatting and type check - black, flake8, mypy, interrogate
   - Run test suite and generate result & test coverage using code climate
   - Check missing docstrings using [interrogate](https://github.com/econchick/interrogate)

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

**Question:** How can i add secrets to repo and test them in workflow?

**Answer:** Secrets are encrypted environment variables that you create in an organization, repository, or repository environment. The secrets that you create are available to use in GitHub Actions workflows. You can read more about how to setup secrets in the repo [here](https://docs.github.com/en/actions/reference/encrypted-secrets)
To use the secret in your workflow file you can simply use an expression: `${{ secrets.YOUR_SECRET_NAME }}` to evaluate your secret in workflow steps.

##

**Question:** How can I execute an additional workflow after this workflow succeeds?

**Answer:** If you want to make a conditional run (stage-wise/sequential) for your existing workflow after successful execution of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) workflow then include following yml code in your existing workflow file on top:

    ```yaml
    on:
     workflow_run:
          workflows: ["CI Workflow"] # name of the workflow you want to execute after
          types:
            - completed
    ```

 In our case, `workflows: ["CI Workflow"]` -  "CI Workflow" is the workflow [name](https://github.com/predictionmachine/pm-gh-actions/blob/ab4b850e81b8cfa2224ab51e29c46c651dfcab72/.github/workflows/pm-gh-actions.yml#L8) of [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)
