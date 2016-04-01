#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
import os
import sys
from sqlalchemy import exc

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    try:
        from core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as I:
        print(I)
    except KeyboardInterrupt:
        print()
    except exc.ProgrammingError:
        print("\033[31;1mdatabase has not initialization\033[0m")
    except exc.InternalError:
        print("\033[31;1mUnknow database,please check database has been created\033[0m")
    except exc.UnboundExecutionError:
        print("\033[31;1mCould not use database engine on this Session\033[0m")
    except exc.OperationalError:
        print("\033[31;1mCan not to connect MySQL server,"
              "\n\tOperation time out"
              "\nor "
              "\n\tAccess denied for user"
              "\nor"
              "\n\tConnection refused, Maybe port cant't be used\033[0m")
