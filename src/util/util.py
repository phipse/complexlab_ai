#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Useful snippets

(c) 2012 - 2013 Peter Schwede
"""
import subprocess
import pynotify


def get_git_branch_string():
    """gets the git branch of the current working directory"""
    args = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    return str(subprocess.check_output(args)).split("\n")[0]


def notify(notifier, string):
    """shows a notification via libnotify. needs pynotify"""
    pynotify.init(notifier)
    notification = pynotify.Notification(string)
    notification.show()


def parse_arg_range(args, type_=int):
    # returns [1,2,3,5,8] e.g. in case of "1-3,5,8"
    res = list()
    for arg in args.split(","):
        if "-" in arg:
            a, b = arg.split("-")
            res += range(type_(min(a, b)), type_(max(a, b))+1)
        else:
            res.append(type_(arg))
    return res
