from fabric.api import cd
from fabric.api import env
from fabric.api import run
from fabric.api import sudo
from fabric.api import task


env.application_name = 'spikes_build'
env.deployment_directory = '/opt'
env.build_directory = 'build'
# env.source_code_directory = 'code_from_git'


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
    run("ps -axf | grep [s]erver-daemon | awk '{ print \"pid:\"$2\", parent-pid:\"$3 }'")


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
    # run('mkdir -p {0}'.format(env.source_code_directory))
    run('git clone https://github.com/eduardoshanahan/spikes_build')

@task
def build():
    """
    Get the code from VCS, get it ready to work and push a tag back to VCS
    """
    with cd(env.source_code_directory):
        sudo('mkdir -p {0}'.format(env.build_directory))


# @task
# def install_kafka():
#     """
#     Get the kafka server ready
#     """
#     import sys
#     sys.path.insert(0, '../../../resources/')
#     from fabric_scripts.scripts import ubuntu, kafka
#     ubuntu.packages.update()
#     kafka.full(configuration='../configuration/kafka')
#     create_kafka_topics()
#     ubuntu.packages.cleanup()
#
#
# @task
# def install_servers(hosts_ip='127.0.0.1', hosts_name='kafka'):
#     """
#     Get the tools for working in the source code
#     """
#     import sys
#     sys.path.insert(0, '../../../resources/')
#     from fabric_scripts.scripts import ubuntu, nginx, nodejs
#     ubuntu.packages.update()
#     ubuntu.hosts.add(hosts_ip, hosts_name)
#     ubuntu.hosts.add('127.0.0.1', 'Logstash') # At the moment keep Logstash on the same machine
#     nginx.full(configuration='../configuration/nginx')
#     nodejs.install()
#     ubuntu.packages.cleanup()
#
#
# @task
# def install_load():
#     """
#     Get ready to load test the servers
#     """
#     import sys
#     sys.path.insert(0, '../../../resources/')
#     from fabric_scripts.scripts import ubuntu
#     ubuntu.packages.update()
#     python.locust.full()
#     ubuntu.packages.cleanup()
#
#
# @task
# def install_log():
#     """
#     Log management
#     """
#     import sys
#     sys.path.insert(0, '../../../resources/')
#     from fabric_scripts.scripts import ubuntu
#     ubuntu.packages.update()
#     logstash.full(configuration='../configuration/logstash')
#     elasticsearch.full(configuration='../configuration/elasticsearch')
#     kibana.full(configuration='../configuration/kibana')
#     ubuntu.packages.cleanup()
#
#
# @task
# def install_single_machine():
#     """
#     All the services in a single machine
#     """
#     import sys
#     sys.path.insert(0, '../../../resources/')
#     from fabric_scripts.scripts import ubuntu, nginx, kafka, nodejs
#     ubuntu.packages.update()
#     ubuntu.hosts.add('127.0.0.1', 'Kafka')
#     ubuntu.hosts.add('127.0.0.1', 'Logstash')
#     nginx.full(configuration='../configuration/nginx')
#     kafka.full(configuration='../configuration/kafka')
#     # logstash.full(configuration='../configuration/logstash')
#     # elasticsearch.full(configuration='../configuration/elasticsearch')
#     # kibana.full(configuration='../configuration/kibana')
#     create_kafka_topics()
#     nodejs.full()
#     nodejs.tools.dtrace.install()
#     ubuntu.packages.cleanup()
#
#
# @task
# def create_kafka_topics():
#     """
#     Create all the topics the platform needs in Kafka
#     """
#     topics = ['company', 'contract', 'supplier', 'user']
#     with cd('/usr/lib/kafka'):
#         for topic in topics:
#             run('bin/kafka-topics.sh --create --zookeeper Kafka:2181 --replication-factor 1 --partitions 1 --topic {0}'.format(topic))
#         run(' bin/kafka-topics.sh --list --zookeeper Kafka:2181')
