#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""


class CommandError(Exception):
    """
    自定义异常错误类型
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):  # 打印时会执行这个方法
        return self.message


def handle_default_options(options, subcommand):
    """
    处理命令行选项,当命令行支持这个参数时.会去判断该方法是否已实现,未实现则抛出异常
    :param options:
    :param subcommand:
    :return:
    """
    package = __import__("core.shortcuts")
    if hasattr(package, 'shortcuts'):
        module = getattr(package, 'shortcuts')
        if hasattr(module, subcommand):
            subcommand = getattr(module, subcommand)
            return subcommand(options)
    raise CommandError("\033[31;1mCommand NotImplementedError\033[0m\n")
