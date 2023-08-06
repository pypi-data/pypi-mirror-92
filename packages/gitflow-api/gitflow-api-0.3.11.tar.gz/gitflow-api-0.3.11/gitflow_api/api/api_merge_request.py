#!/usr/bin/env python
# encoding: utf-8

import abc
import os


class ApiMergeRequest(object):
    __metaclass__ = abc.ABCMeta

    global path
    global gl

    def __init__(self, gl):
        self.path = os.getcwd()
        self.gl = gl

    @abc.abstractmethod
    def find_merge_request_by_url_and_branch(self, git_url, branch):
        return

    @abc.abstractmethod
    def create_merge_request(self, git_url, branch_from, title, description, issue_id, to_branch, label):
        return

    @abc.abstractmethod
    def validate_and_close_merge_request(self, git_url, branch):
        pass

    @abc.abstractmethod
    def validate_merge_request_by_url_and_branches(self, git_url, branch_from, branch_to):
        pass

    @abc.abstractmethod
    def find_merge_request_by_commit_message(self, commit_message):
        return
