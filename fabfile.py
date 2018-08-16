from fabric.api import local, cd, run, env

env.hosts = ['production']


def deploy():
    local('git push')
    with cd('~/getpayslip'):
        run('git pull')
        run('pipenv install')
