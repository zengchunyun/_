#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import sys
import os
import argparse


try:
    from conf.settings import subcommands
    from core.views import handle_default_options, CommandError
except ImportError:
    pass


class ManagementUtility(object):
    """
    管理组件,该功能处理命令行输入,处理非法输入
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]  # 获取命令行输入
        self.prog_name = os.path.basename(self.argv[0])

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'

        parser = argparse.ArgumentParser(usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('args', nargs='*')
        try:
            args = parser.parse_known_args(self.argv[2:])
            try:
                if len(self.argv) < 2:
                    self.error_msg()
                elif subcommand not in subcommands.values():
                    raise CommandError("\033[31;1mCommand not found\033[0m\n")
            except NameError:
                print("\033[31;1m[subcommands] is not define ,please check the settings\033[0m")
                return False

            handle_default_options(self.argv[2:], subcommand)
        except CommandError as e:
            print(e)
            self.error_msg()

    @staticmethod
    def error_msg():
        """
        打印帮助信息
        :return:
        """
        print('\033[31;1m[myfort]\033[0m')
        list(map(lambda argv: print(str('\t{}'.format(subcommands[argv])).expandtabs(tabsize=4)), subcommands))
        exit(1)


def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()
