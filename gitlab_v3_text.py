#!/usr/bin/python
# -*- coding: UTF-8 -*-
# python-gitlab 版本 14.0

import gitlab
import os
import json
import subprocess

from logger import get_logger

from config import GITLAB_TOKEN
from config import GITLAB_HOST


class GitlabAPI(object):
    def __init__(self, *args, **kwargs):
        self.gl = gitlab.Gitlab(GITLAB_HOST, private_token=GITLAB_TOKEN, api_version='3')

    def get_all_group(self):
        """
        获取所有群组
        :return:
        """
        return self.gl.groups.list(all=True)

    def get_user_byname(self, username):
        return self.gl.users.list(username=username)[0]

    def get_by_projectid(self, project_id):
        return self.gl.projects.get(project_id)


class CheckGitProject(GitlabAPI):
    """
        检查项目
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_id = kwargs.get("project_id")
        self.branch = kwargs.get("branch")
        self.logger = get_logger(log_dir=os.path.join(os.path.abspath('.'), 'commit_log'), log_filename="commit_log.log")


    def get_commits(self):
        project = self.get_by_projectid(self.project_id)
        if not project:
            raise ValueError(f"project is none: {project}")
        # branch = project.branches.get(self.branch)
        # get commit list
        commits = project.commits.list(ref_name=self.branch)
        commit = commits[0]
        return {
            "author_email": commit.author_email,
            "author_name": commit.author_name,
            "committer_email": commit.committer_email,
            "committer_name": commit.committer_name,
            "created_at": commit.created_at,
            "title": commit.title,
            "message": commit.message,
        }

    def insert(self, filepath: str, data: dict) -> bool:
        """
        :param filepath: 文件路径
        :param data:    保存json 数据
        :return: True/Fasle
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as dump_f:
                json.dump(data, dump_f, indent=4, sort_keys=True)
            self.logger.info("commit 数据保存成功")
            return True
        except Exception as e:
            return False

    def open_(self, filepath) -> dict:
        """
        :param open_dir: 打开文件夹
        :param filename:  文件名
        :return: json 数据
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"filepath: {filepath} is not exists")
        with open(filepath, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        return load_dict

    def execute_local_shell_cmd(self, cmd):
        status, result = subprocess.getstatusoutput(cmd)
        result = result.split("\n")
        return status, result

    def check_message(self):
        commit = self.get_commits() # 最新commit json数据
        base_dir = os.path.join(os.path.abspath('.'), "commit")
        filename = "commit.json"
        if not os.path.exists(base_dir):
            os.makedirs(base_dir, exist_ok=True)
        path = os.path.join(base_dir, filename)
        if not commit:
            self.logger.error("commit 信息为 空")
            raise ValueError("commit 信息为 空")

        old_commit_info = self.open_(filepath=path)
        if all([commit.get('created_at'), commit.get('created_at')]):
            if commit.get('created_at') > old_commit_info.get('created_at'):
                # TODO 判断 git 目录是否 存在 存在 更新
                shell_path = os.path.join(os.path.abspath('.'), "git_pull.sh")
                shell = 'sh ' + shell_path
                status_st, output_st = subprocess.getstatusoutput(shell)
                if status_st != 0:
                    self.logger.error(
                        f" git_pull.sh 脚本执行失败: {status_st}"
                        f" output_st: {output_st}"
                                      )
                else:
                    self.logger.info(
                        f" git_pull.sh 脚本执行成功: {status_st}"
                        f" output_st: {output_st}"
                    )
                if not self.insert(data=commit, filepath=path):
                    self.logger.error("commit 数据保存失败")

if __name__ == '__main__':
    git = CheckGitProject(**{
        "project_id": 23,
        "branch": "dev",
    })
    git.check_message()

    # save_dir = os.path.join(os.path.abspath('.'), "commit")
    # filename = "commit.json"
    # if not os.path.exists(save_dir):
    #     os.makedirs(save_dir, exist_ok=True)
    # path = os.path.join(save_dir, filename)
    # data = {'author_email': '1360082963@qq.com', 'author_name': '段伟业', 'committer_email': '1360082963@qq.com',
    #         'committer_name': '段伟业', 'created_at': '2021-02-25T17:37:34.000+08:00', 'title': 'log 文件夹保留',
    #         'message': 'log 文件夹保留\n'}
    # git.insert(filepath=path, data=data)
    # git.open_(save_dir, filename="commit.json")
    # all_group = git.get_all_group()
    # print(f"all_group: {all_group}")
    # project_id = 23
    # # projects = git.gl.projects.list()
    # project = git.gl.projects.get(project_id)
    # print(f"project: {project}")
    # branch = project.branches.get('master')
    # print(f"branch: {branch}")
    # commits = branch.commits.list()
    # commits = project.commits.list(all=True,
    #                                query_parameters={'ref_name': 'dev'}
    #                                )
    # commits = project.commits.list(ref_name="dev")
    # print(f"commits: {commits}")
    # for c in commits:
    #     print(c.author_name, c.message, c.title)
    # for project in projects:
    #     print(project.id)
    #     print(project.name)
    #     print(project.path_with_namespace)
    # print(projects)
