# pm-gh-actions
Repository for common GitHub Actions workflows for Prediction Machine

 - - -

### main.yml

#### How it works:

-  Run the checks (as mentioned in the pm-coding-template) as a CI build process (it can be used in other repo's)
-  This workflow uses the configuration files for flake8, mypy and pystest from the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template) - it clones the `pm-coding-template` repo during the build process and uses the config files from the repo.

#### The check included in the CI build for workflow file is:
   - Check for empty PR description.
   - Check for unwanted files - .zip etc.
   - Check hardcoded credentials in files.
   - Linting and type check - flake8, black, mypy
   - Run test suit and generate result + test coverage (using code climate)
   - Check missing docstrings using [interrogate](https://github.com/econchick/interrogate)
   - The config file + the requirements.txt file used during the CI builds are fetched from [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) dynamically.

**Note**: For above mentioned checks the `github-actions` bot will comment the respective issues/check fails.

### Things to remember:
- Please make sure to replace `CC_TEST_REPORTER_ID` with your respective repo reporter id. (can find on code climate portal)
- If you want to integrate `main.yml` to your repo then make sure to copy this file and move to `.github/workflows/` directory.
- If you want to make conditional run (stage wise/sequential) for your existing workflow after a successful execution of `main.yml` workflow then include following yml code in your existing workflow file:

```yaml
on:
 workflow_run:
      workflows: ["CI Workflow"] # name of the workflow you want to execute after
      types:
        - completed
```

In our case, `workflows: ["CI Workflow"]` -  "CI Workflow" is the workflow name of `main.yml`

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
