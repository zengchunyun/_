#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import logging

#
# logging.warning("user hello")
# logging.critical("75")
#
logging.basicConfig(filename="acces8s.log", level=logging.INFO,
                    format='%(asctime)s %(message)s')
logging.warning("heled")
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

# logger = logging.getLogger('TEST-LOG')
# logger.setLevel(logging.DEBUG)
#
#
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
#
#
# fh = logging.FileHandler("assecc.log")
# fh.setLevel(logging.WARNING)
#
#
# formatter = logging.Formatter("%(asctime)s - %(name)s  - %(levelname)s  - %(message)s")
#
#
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
#
#
# logger.addHandler(ch)
# logger.addHandler(fh)
#
#
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
