import os
import subprocess


from django.core.management import call_command


def get_git_revision_hash(short=True):
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short' if short else '--short=500', 'HEAD']).decode(
            'utf-8').strip('\n')
    except Exception as e:
        print(e)


def get_last_commit_date():
    try:
        return subprocess.check_output(['git', 'log', '-1', '--format=%cd']).decode('utf-8').strip('\n')
    except Exception as e:
        print(e)


def updated_to_upstream():
    from github import Github
    AUTHTOKEN = os.environ.get('UPSTREAM_GITHUB_AUTHTOKEN')
    BRANCH = "master"
    REPO = os.environ.get('UPSTREAM_GITHUB_REPO')

    if all([AUTHTOKEN, BRANCH, REPO]):
        github = Github(AUTHTOKEN)
        if github:
            commit = github.get_repo(REPO).get_branch(BRANCH).commit.sha
        else:
            commit = None
        local_commit = get_git_revision_hash(short=False)
        return local_commit == commit


def is_pending_migration():
    from io import StringIO

    result = []
    out = StringIO()
    call_command('showmigrations', format="plan", stdout=out)
    out.seek(0)
    for line in out.readlines():
        status, name = line.rsplit(' ', 1)
        result.append((status.strip() == '[X]', name.strip()))
    return any(filter(lambda item: not item[0], result))


def is_database_changes():
    from io import StringIO

    out = StringIO()
    call_command('makemigrations', check=True, dry_run=True, stdout=out)
    out.seek(0)
    return not ('No changes detected' in out.read())
