#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN', '')
GITLAB_HOST = os.environ.get('GITLAB_HOST', 'http://')
GITLAB_Branch_Path = os.environ.get('GITLAB_Branch_Path', 'TaxPlatform/')
