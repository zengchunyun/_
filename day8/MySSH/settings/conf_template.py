#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import configparser


class MakeConf(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def write(self, section, **kwargs):
        self.config.read(self.filename)
        if section in self.config.sections():
            self.update(section, **kwargs)
        else:
            self.config[section] = {}
            self.set_conf(section, **kwargs)
            self.make(mode="w")

    def read(self, section=None, option=None):
        self.config.read(self.filename)
        if section:
            if option:
                return self.config.get(section, option)
            else:
                return list(self.config[section].keys())
        return self.config.sections()

    def update(self, section, **kwargs):
        self.config.read(self.filename)
        if section not in self.config.sections():
            self.config.add_section(section)
        self.set_conf(section, **kwargs)
        self.make()

    def make(self, mode="w"):
        with open(self.filename, mode) as configfile:
            self.config.write(configfile)

    def set_conf(self, section, **kwargs):
        for key, value in kwargs.items():
            self.config.set(section, key, value)


def initconf():
    new_conf = MakeConf("settings.ini")
    new_conf.write("nginx", **{"bj01": "127.0.0.1"})
    new_conf.write("nginx", **{"bj02": "192.168.11.1"})
    new_conf.write("nginx", **{"bj04": "127.0.0.1"})
    new_conf.write("nginx", **{"bj03": "127.0.0.1"})
    new_conf.write("nginx", **{"bj04": "127.0.0.1"})
    new_conf.write("nginx", **{"bj05": "127.0.0.1"})
    new_conf.write("tomcat", **{"bj02": "127.0.0.2"})
    new_conf.write("op", **{"bj02": "127.0.0.2"})
    new_conf.write("db", **{"bj01": "127.0.0.1", "sh01": "127.0.0.1"})
    new_conf.write("mem")

    print(new_conf.read("nginx"))

if __name__ == "__main__":
    initconf()