# pm-gh-actions
Repository for common GitHub Actions workflows for Prediction Machine

 - - -

## main.yml

#### How it works:

- Run the checks (as mentioned in the pm-coding-template) as a CI build process (it can be used in other repo's)
- This workflow uses the configuration files for flake8, mypy and pytest from the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template). It clones the `pm-coding-template` repo during the build process and uses the config files present in the repo.

#### The check included in the CI build for workflow file is:
   - Check for empty PR description.
   - Check for unwanted files - .zip etc.
   - Check hardcoded credentials in files.
   - Linting and type check - flake8, black, mypy
   - Run test suit and generate result + test coverage (using code climate)
   - Check missing docstrings using [interrogate](https://github.com/econchick/interrogate)
   - The config file and the requirements.txt file used during the CI builds are fetched from [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) dynamically.

**Note**: For above-mentioned checks, the `github-actions` bot will comment the respective issues/check fails on PR.

### Installation instructions:

- To use `main.yml` in your project repo, copy `main.yml` from this repo, and paste it in `.github/workflows/` folder of project repo.
- Once you have copied the `main.yml` to `.github/workflows/`, please make sure to change the value of `CC_TEST_REPORTER_ID` ENV variable to your repo reporter id in `main.yml`. `CC_TEST_REPORTER_ID` is being used for reporting the test coverage to code climate.
- Each repo has a unique `CC_TEST_REPORTER_ID`, which can be obtained from repo setting page assuming that code climate is already configured for your repo.
- Once the above steps are done you can run the workflow and test. You don't need to set up any other secrets like `GITHUB_TOKEN` for `main.yml` to work. (see FAQ)
- If you need `main.yml` to use different configuration for for mypy, flake8, black and pytest then you can define then in the workflow file as bwlow:
  - For mypy, replace the value of `mypy_flags: '--config-file=pm-coding-template/mypy.ini'` to your config file from the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L130)
  - For flake8, replace the value of `flake8_args: '--config=pm-coding-template/.flake8'` to your config file from the repo. [see here](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L118)
  - For black configuration add the `black_args: '--config=path_to_your_configfile'`. This workflow uses default configuration provided by black.
  - For pytest, you need to add configuration file path to [this](https://github.com/predictionmachine/pm-gh-actions/blob/1be9b2cefc0f3f38614fca87d966feb4eeb4b2bb/.github/workflows/main.yml#L138) command in `main.yml` file.
- Please see FAQ section if you have any questions, feel free to raise an issue if you don't find an answer to your question.
- - -

### Few screenshots from the PR:

- Empty PR Description check:
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
**Question:** Do i need to setup `GITHUB_TOKEN` in repo secret? it's being used in `main.yml`

**Answer:** No. GitHub automatically creates a GITHUB_TOKEN secret to use in your workflow. You can use the `GITHUB_TOKEN` to authenticate in a workflow run.
When you enable GitHub Actions, GitHub installs a GitHub App on your repository. The`GITHUB_TOKEN` secret is a GitHub App installation access token. You can use the installation access token to authenticate on behalf of the GitHub App installed on your repository. The token's permissions are limited to the repository that contains your workflow. Before each job begins, GitHub fetches an installation access token for the job. The token expires when the job is finished.
You can read more about this [here](https://docs.github.com/en/actions/reference/authentication-in-a-workflow)

## 
**Question:** Which configurations are being used for mypy, flake8 and other check in the workflow?

**Answer:** This workflow uses the configuration files present in the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) repo. The workflow run clones `pm-coding-template` the repo and uses the config files from it. If you need to use your configuration file then add the path of configuration file in the `main.yml` under the respective step, as a parameter.
See the installation instruction to know more about it.

##
**Question:** How can i add secrets to repo ad test them in workflow?

**Answer:** Secrets are encrypted environment variables that you create in an organization, repository, or repository environment. The secrets that you create are available to use in GitHub Actions workflows. You can read more about how to setup secrets in the repo [here](https://docs.github.com/en/actions/reference/encrypted-secrets)
To use the secret in your workflow file you can simply use an expression: `${{ secrets.YOUR_SECRET_NAME }}` to evaluate your secret in workflow steps.

##
**Question:** How can I execute both the workflow satge-wise/sequentially?

**Answer:** If you want to make a conditional run (stage-wise/sequential) for your existing workflow after successful execution of `main.yml` workflow then include following yml code in your existing workflow file:

    ```yaml
    on:
     workflow_run:
          workflows: ["CI Workflow"] # name of the workflow you want to execute after
          types:
            - completed
    ```

 In our case, `workflows: ["CI Workflow"]` -  "CI Workflow" is the workflow name of `main.yml`

