from fabric.api import local, cd, run, env, prefix

env.hosts = ['sdelquin.me']


def deploy():
    local('git push')
    with prefix('source ~/.virtualenvs/getpayslip/bin/activate'):
        with cd('~/code/getpayslip'):
            run('git pull')
            run('pip install -r requirements.txt')
