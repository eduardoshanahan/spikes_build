from fabric.api import local
from fabric.api import task
from fabric.api import warn_only
from fabric.api import lcd
from fabric.api import env

env.repositories = [
    ('https://github.com/eduardoshanahan/fabric_scripts', './git_resources/fabric_scripts')
]

@task
def git_clone():
    """
    Clone resources
    """
    for repository in env.repositories:
        with warn_only():
            local('git clone {0} {1}'.format(repository[0], repository[1]))


@task
def git_pull():
    """
    Pull resources
    """
    for repository in env.repositories:
        with lcd(repository[1]):
            local('git pull')
