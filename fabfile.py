from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm


env.hosts = ['gdevine@puma.nerc.ac.uk']


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
        run("pip install -r requirements.txt")
        run("cd cv_translator")
        run("chmod 777 cv_translator.sqlite")

