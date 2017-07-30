from fabric.api import local, prefix, cd, run, env

env.hosts = ["production"]


def deploy():
    local("git push")
    with prefix("source ~/.virtualenvs/getpayslip/bin/activate"):
        with cd("~/getpayslip"):
            run("git pull")
            run("pip install -r requirements.txt")
