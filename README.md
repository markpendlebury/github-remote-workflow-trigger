# GitHub Remote Workflow Trigger

A minimal example of triggering a GitHub Actions workflow remotely from Python using [PyGithub](https://github.com/PyGithub/PyGithub).

## What it demonstrates

- `.github/workflows/workflow.yml` defines a workflow with a `workflow_dispatch` trigger that accepts one input (`my_input`) and echoes it.
- `workflow_trigger.py` authenticates to GitHub, resolves the repository and workflow, dispatches the workflow on a chosen branch, then polls for the run to start and reports its URL and status.

## Prerequisites

- Python 3.8+
- PyGithub 2.x (the script uses `github.Auth.Token`)

```bash
pip install -r requirements.txt
```

## Usage

1. Generate a GitHub personal access token (PAT) with the `workflow` scope (add `repo` if the repository is private).
2. Set the environment variables:

| Variable | Description |
| --- | --- |
| `GITHUB_TOKEN` | Your GitHub PAT |
| `MY_INPUT` | Any string, e.g. `Hello World` |
| `REPOSITORY` | Repository name as `owner/repo` |
| `WORKFLOW_FILENAME` | Workflow filename, e.g. `workflow.yml` |
| `BRANCH` | Branch to run the workflow on, e.g. `main` |

3. Run it:

```bash
python workflow_trigger.py
```

The script prints the authenticated user, repository and workflow name, dispatches the workflow, then polls until the run appears and prints its URL and status.
