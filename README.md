# pm-gh-actions
Repository for common GitHub Actions workflows for Prediction Machine

### main.yml

#### How it works:

-  Run the checks (as mentioned in the pm-coding-template) as a CI build process (it can be used in other repo's)
-  This workflow uses the configuration files for flake8, mypy and pystest from the [pm-coding-template](https://github.com/predictionmachine/pm-coding-template) - it clones the `pm-coding-template` repo during the build process and uses the config files from the repo.

#### The check included in the CI build for workflow file is:
   - Check for empty PR description.
   - Check for unwanted files - .zip etc.
   - Check hardcoded credentials in files.
   - Linting and type check - flake8, black, mypy
   - Run test suit and generate result + test coverage
   - Check missing docstrings using.
   - The config file + the requirements.txt file used during the CI builds are fetched from [pm-coding-template](https://github.com/predictionmachine/pm-coding-template/) dynamically.
**Note**: For above mentioned checks the `github-actions` bot will comment the respective issues/check fails.

#### Screenshots from the PR:

![empty-pr](docs/screenshots/empty-pr-comment.png?raw=true "Empty PR comment")
![Alt text](docs/screenshots/black-report.png?raw=true "black")
![Alt text](docs/screenshots/docstring-report.png?raw=true "docstring")
![Alt text](docs/screenshots/flake8-report.png?raw=true "flake8")
![Alt text](docs/screenshots/mypy-report.png?raw=true "mypy")
![Alt text](docs/screenshots/pytest-coverage-report.png?raw=true "pytest-cov")
![Alt text](docs/screenshots/secrets_report.png?raw=true "secret-report")
![Alt text](docs/screenshots/unit-test-res.png?raw=true "unit-test")

#### The GH action from marketplace used are:
- [reviewdog](https://github.com/reviewdog) - for flake8, black, hard code credentials and mypy
- [sticky-pull-request-comment](https://github.com/marocchino/sticky-pull-request-comment) - for PR comments.
- [pytest-coverage-commentator](coroo/pytest-coverage-commentator) - for pytest coverage comments.
