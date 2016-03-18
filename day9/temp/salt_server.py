#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: zengchunyun
"""
# import salt
#
# <Salt ID>:       # The id to reference the target system with
#     host:        # The IP address or DNS name of the remote host
#     user:        # The user to log in as
#     passwd:      # The password to log in with
#
#     # Optional parameters
#     port:        # The target system's ssh port number
#     sudo:        # Boolean to run command via sudo
#     tty:         # Boolean: Set this option to True if sudo is also set to
#                  # True and requiretty is also set on the target system
#     priv:        # File path to ssh private key, defaults to salt-ssh.rsa
#                  # The priv can also be set to agent-forwarding to not specify
#                  # a key, but use ssh agent forwarding
#     timeout:     # Number of seconds to wait for response when establishing
#                  # an SSH connection
#     minion_opts: # Dictionary of minion opts
#     thin_dir:    # The target system's storage directory for Salt
#                  # components. Defaults to /tmp/salt-<hash>.
#     cmd_umask:   # umask to enforce for the salt-call command. Should be in
#                  # octal (so for 0o077 in YAML you would do 0077, or 63)



# ext_pillar:
#   - example_a: some argument
#   - example_b:
#     - argumentA
#     - argumentB
#   - example_c:
#       keyA: valueA
#       keyB: valueB


import logging
log = logging.getLogger(__name__)


try:
    import weird_thing
    EXAMPLE_A_LOADED = True
except ImportError:
    EXAMPLE_A_LOADED = False


__opts__ = { 'example_a.someconfig': 137 }


def __init__( __opts__ ):
    # Do init work here


# This external pillar will be known as `example_a`
def __virtual__():
    if EXAMPLE_A_LOADED:
        return True
    return False


# This external pillar will be known as `something_else`
__virtualname__ = 'something_else'

def __virtual__():
    if EXAMPLE_A_LOADED:
        return __virtualname__
    return False

ext_pillar( id, pillar, 'some argument' )                   # example_a
ext_pillar( id, pillar, 'argumentA', 'argumentB' )          # example_b
ext_pillar( id, pillar, keyA='valueA', keyB='valueB' } )    # example_c


def ext_pillar( minion_id, pillar, *args, **kwargs ):

    my_pillar = {'external_pillar': {}}

    my_pillar['external_pillar'] = get_external_pillar_dictionary()

    return my_pillar

salt-call '*' pillar.get external_pillar


ext_pillar:
  - cmd_json: 'echo {\"arg\":\"value\"}'