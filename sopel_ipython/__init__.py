# coding=utf-8
"""
ipython.py - Sopel IPython Console Module
Copyright © 2014, Elad Alfassa <elad@fedoraproject.org>
Copyright © 2022, dgw, technobabbl.es
Licensed under the Eiffel Forum License 2.

https://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import sys

import sopel
import sopel.module

from IPython.terminal.embed import InteractiveShellEmbed


console = None


@sopel.module.commands('console')
@sopel.module.require_admin('Only admins can start the interactive console')
def interactive_shell(bot, trigger):
    """Starts an interactive IPython console"""
    global console
    if bot.memory.get('iconsole_running', False):
        bot.say('Console already running')
        return
    if not sys.__stdout__.isatty():
        bot.say('A tty is required to start the console')
        return
    if bot._daemon:
        bot.say('Can\'t start console when running as a daemon')
        return

    # Backup stderr/stdout wrappers
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    # IPython wants actual stderr and stdout
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    banner1 = 'Sopel interactive shell (embedded IPython)'
    banner2 = '`bot` and `trigger` are available. To exit, type exit'
    exitmsg = 'Interactive shell closed'

    console = InteractiveShellEmbed(banner1=banner1, banner2=banner2,
                                    exit_msg=exitmsg)

    bot.memory['iconsole_running'] = True
    bot.say('console started')
    console()
    bot.memory['iconsole_running'] = False

    # Restore stderr/stdout wrappers
    sys.stdout = old_stdout
    sys.stderr = old_stderr
