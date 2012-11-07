from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


env.hosts = ['gdevine@puma.nerc.ac.uk']
env.activate = 'source /home/gdevine/web/prod/cv_translator/venv/bin/activate'

def gitupdate():
    local("git add .")
    local("git add -u")
    local("git commit")
    local("git push")


def deploy():
    code_dir = '/home/gdevine/web/prod/cv_translator'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@github.com:gerarddevine/CV_Translator.git %s" % code_dir)
    with cd(code_dir):
        run("pwd")
        run("ls -la")
        run("git pull")
        run("virtualenv venv --no-site-packages")
        run(env.activate + "&& pip install -r requirements.txt")
        run(env.activate + "cd cv_translator")
        run(env.activate + "python manage.py syncdb --noinput")
        run(env.activate + "chmod 777 cv_translator.sqlite")

