#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : mi_run
# @Time         : 2020/11/10 6:12 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

"""
'console_scripts': [
    'mi-run=mi.mi_run:cli',
]
"""
import os
import fire
from pathlib import Path
from mi.utils import get_module_path
from meutils.pipe import *




class Cli(object):
    """doc"""

    def __init__(self, **kwargs):
        pass

    def tasks_list(self, tasks='tasks'):
        return list(Path(get_module_path(f'../{tasks}', __file__)).glob('*'))

    def task(self, app_file='demo.py', nohup=0, python='python'):
        """mi-run - task xindao_ann"""
        if '/' not in app_file:
            app_file = list(Path(get_module_path('../tasks', __file__)).glob(f'*{app_file}*'))[0]
        cmd = f"{python} {app_file}"
        self._run_cmd(cmd, nohup)

    def _run_cmd(self, cmd, nohup=0):
        cmd = f"nohup {cmd} &" if nohup else cmd
        return os.system(cmd)


class DslCli(object):
    def debug(self, path='dsl3'):
        """编译dsl3项目， 生成debug执行文件"""

        if not Path('dsl3').exists():
            magic_cmd("git clone git@git.n.xiaomi.com:feeds-recommend-cpp/dsl3.git")
        else:
            magic_cmd("cd dsl3 && sh release.sh")





cli = lambda: fire.Fire(Cli)
dsl_cli = lambda: fire.Fire(DslCli)

if __name__ == '__main__':
    print(Cli().tasks_list())
