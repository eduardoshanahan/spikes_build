from fabric.api import cd
from fabric.api import env
from fabric.api import get
from fabric.api import lcd
from fabric.api import local
from fabric.api import put
from fabric.api import run
from fabric.api import settings
from fabric.api import sudo
from fabric.api import task
import datetime
import os

env.application_name = 'spikes_build'
env.deployment_directory = '/opt'
env.application_code_directory = 'code'
env.build_directory = 'build'

@task
def at_vagrant():
    """
    Connect with Vagrant
    """
    import sys
    sys.path.insert(0, '../git_resources/')
    from fabric_scripts.scripts import vagrant
    vagrant.connect()


@task
def list_processes():
    """
    List each process running in parallel
    """
    run("ps axo ppid,pid,command | grep [s]erver-daemon")


@task
def prepare_machine():
    """
    All the tools in a single machine
    """
    import sys
    sys.path.insert(0, '../git_resources/')
    from fabric_scripts.scripts import ubuntu, nodejs, git
    ubuntu.packages.update()
    git.install()
    nodejs.full()
    ubuntu.packages.cleanup()


@task
def get_source_code():
    """
    Call git and get the source code
    """
    with settings(warn_only=True):
        run('git clone https://github.com/eduardoshanahan/spikes_build')
        run('git pull')


@task
def build():
    """
    Get the code from VCS, get it ready to work and push a tag back to VCS
    """
    with cd(env.application_name), cd (env.application_code_directory):
        run('npm install')
        # version = 'build_{0}'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M'))
        # run('git tag {0}'.format(version))
        # run('git push origin {0}'.format(version))


@task
def get_build():
    """
    Move the files into the build directory
    """
    local('rm -rf {0}'.format(env.build_directory))
    local('mkdir -p {0}'.format(env.build_directory))
    with lcd(env.build_directory):
        with cd(env.application_name), cd (env.application_code_directory):
            get('node_modules', './')
            get('bin', './')
            get('lib', './')
            get('configuration', './')


@task
def deploy():
    """
    Drop all the artifacts in the deployment directory
    """
    destination = os.path.join(env.deployment_directory, env.application_name)
    sudo('mkdir -p {0}'.format(destination))
    with lcd(env.build_directory):
        put('node_modules', destination, use_sudo=True)
        put('bin', destination, use_sudo=True)
        put('lib', destination, use_sudo=True)

@task
def configure():
    """
    Pass files for upstart
    """
    origin = os.path.join(env.build_directory, 'configuration', env.application_name)
    with lcd(origin):
        put('etc', '/', use_sudo=True)
    # prepare_daemons()


# @task
# def prepare_daemons():
#     """
#     Make the daemons executable
#     """
#     destination = os.path.join(env.deployment_directory, env.application_name, 'bin')
#     with cd(destination):
#         sudo('chmod +x server-daemon')

@task
def start():
    """
    Start the daemons
    """
    sudo('start server-daemon')


@task
def cleanup():
    """
    Remove temporary directories
    """
    local('rm -rf {0}'.format(env.build_directory))
