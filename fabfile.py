from fabric.api import local
from fabric.api import task
from fabric.api import warn_only
from fabric.api import lcd
from fabric.api import env

env.repositories = [
    ('https://github.com/eduardoshanahan/fabric_scripts', './git_resources/fabric_scripts')
]

@task
def get_git_resources():
    """
    Grab any tools needed from the repository
    """
    with warn_only():
        for repository in env.repositories:
            local('git clone {0} {1}'.format(repository[0], repository[1]))
            with lcd(repository[1]):
                local('git pull')

