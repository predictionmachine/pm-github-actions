# pm-gh-actions
<<<<<<< HEAD
Repository for sanity checking and nicely commenting on pull requests for python repositories.
Provides a GitHub Actions workflow file which you can customize. By default, assumes you are a fan of
`black` (for layout), `flake8` for further pip8 conformance, `mypy` for typechecking, and `pytest` and _codeclimate quality_ for testing and coverage.
Developed and used by _Prediction Machine_.
=======

Repository for common GitHub Actions workflows for Prediction Machine
>>>>>>> 884c046 (Fix markdown linting in readme)

 - - -

## [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml)

#### How it works:

- Run the checks (as mentioned in the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template)) as a CI build process (it can be used in other repo's)
- This workflow uses the configuration files for flake8, mypy and pytest from the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template). It clones the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template) repo during the build process and uses the config files present in the repo.

#### The check included in the CI build for workflow file is:
   - Check for empty PR description.
   - Check for unwanted files - .zip etc.
   - Check hardcoded credentials in files.
   - Linting and type check - flake8, black, mypy
   - Run test suit and generate result & test coverage using code climate)
   - Check missing docstrings using [interrogate](https://github.com/econchick/interrogate)
   - The config file and the requirements.txt file used during the CI builds are fetched from [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) dynamically.

**Note**: For the above-mentioned checks, the `github-actions` bot will comment on the respective issues/check fails on PR.

### Installation instructions:

- To use `main.yml` in your project repo, copy `main.yml` from this repo, and paste it in the `.github/workflows/` folder of your project repo.
- Once you have copied the `main.yml` to `.github/workflows/` folder, set the value of `CC_TEST_REPORTER_ID` in `main.yml`. The value is used for reporting the test coverage to code climate, to your repo specific reporter id. See [finding your test coverage token](https://docs.codeclimate.com/docs/finding-your-test-coverage-token) for obtaining the id.
- Once the above steps are done you can run the workflow and test. You don't need to set up any other secrets like `GITHUB_TOKEN` for `main.yml` to work.
- For coverage run, this workflow assumes `test` folder to be present in the repo else it will fail. If you want to add different folder for coverage then you need to edit this `coverage run --source=test -m pytest` command in `main.yml` [here](https://github.com/predictionmachine/pm-docker-images/blob/cf4df6bfc1c6b5b630b8d9a7fcde08a639e4c8db/.github/workflows/ci.yml#L139) and replace `test` with your folder name.
- If you need `main.yml` to use different configuration files for mypy, flake8, black and pytest, then you can define them in the workflow file as below:
  - For mypy, replace the value of `mypy_flags: '--config-file=pm-coding-template/mypy.ini'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L130)
  - For flake8, replace the value of `flake8_args: '--config=pm-coding-template/.flake8'` to your config file present in the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L118)
  - For black configuration add the `black_args: '--config=path_to_your_configfile'` in `main.yml` under `with` [tag](https://github.com/predictionmachine/pm-docker-images/blob/cf4df6bfc1c6b5b630b8d9a7fcde08a639e4c8db/.github/workflows/ci.yml#L122). This workflow uses default configuration provided by black.
  - For pytest, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L138) command in `main.yml` file.
- Please see FAQ section if you have any questions, feel free to raise an issue if you don't find an answer to your question.

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
- [reviewdog](https://github.com/reviewdog) - for flake8, black, hard code credentials and mypy
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

**Question:** Which configurations are being used for mypy, flake8 and other check in the workflow by default?

**Answer:** This workflow uses the configuration files present in the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) repo. The workflow run clones [pm-coding-template](https://github.com/predictionmachine/pm-coding-template) repo and uses the config files from it. If you need to use your configuration file then add the path of configuration file in the [pm-gh-actions.yml](.github/workflows/pm-gh-actions.yml) under the respective step, as a parameter.
See the [installation instruction]("#Installation-instructions") to know more about it.

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
