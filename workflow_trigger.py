import os
import sys
import time

from github import Auth, Github


def get_env(name):
    """Return a required environment variable, or exit with a clear message."""
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


def trigger_workflow():
    """Trigger a GitHub Actions workflow and confirm the run was created."""
    github_token = get_env("GITHUB_TOKEN")
    my_input = get_env("MY_INPUT")
    repository = get_env("REPOSITORY")
    workflow_filename = get_env("WORKFLOW_FILENAME")
    branch = get_env("BRANCH")

    github = Github(auth=Auth.Token(github_token))
    print(f"Authenticated as {github.get_user().login}")

    repo = github.get_repo(repository)
    print(f"Repository: {repo.full_name}")

    workflow = repo.get_workflow(workflow_filename)
    print(f"Workflow: {workflow.name}")

    # Count runs on this branch before dispatching so we can detect the new one.
    runs_before = workflow.get_runs(branch=branch).totalCount

    # create_dispatch returns True on success and False on failure.
    dispatched = workflow.create_dispatch(ref=branch, inputs={"my_input": my_input})
    if not dispatched:
        sys.exit("Failed to create the workflow dispatch.")

    # The dispatch is async — poll until a new run appears on the branch.
    for _ in range(30):
        runs = workflow.get_runs(branch=branch)
        if runs.totalCount > runs_before:
            run = runs[0]  # runs are newest-first
            print(f"Run started: {run.html_url} (status: {run.status})")
            return
        time.sleep(5)

    sys.exit("Timed out waiting for the workflow run to start.")


if __name__ == "__main__":
    trigger_workflow()
