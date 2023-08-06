#!/usr/bin/env python
# encoding: utf-8
import shutil
from subprocess import check_call

from gitflow_api.deploy.deploy import Deploy


class Pypi(Deploy):

    def __init__(self):
        super(Pypi, self).__init__(Pypi.__class__)
        self.__qualname__ = 'Pypi'

    def deploy(self):
        # remove dist and build files
        try:
            shutil.rmtree('dist')
            shutil.rmtree('build')
        except FileNotFoundError:
            print('Skipping deleting folder')

        cmd = 'python3 setup.py sdist'
        check_call(cmd, shell=True)

        cmd = 'twine upload dist/*'
        check_call(cmd, shell=True)
