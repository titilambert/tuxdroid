# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import time
import subprocess
from nestor import TuxAction, NestorPlugin

#ID    Done  ETA       Up      Down    Ratio  Status       Name


class TransmissionMonitor(TuxAction):

    def split(self, info):
        rval, start = [], 0
        for offset in (4, 10, 22, 30, 38, 45, 58, -1):
            if offset == -1:
                offset = None
            rval.append(info[start:offset].strip())
            start = offset
        return rval

    def action(self, tux):
        p = subprocess.Popen(['transmission-remote', 'smarties', '-l'],
                             stdout=subprocess.PIPE)
        torrents = (self.split(t)
                    for t in p.communicate()[0].split('\n')[1:-1])

        to_speak = []
        for torrent in torrents:
            title, status, done = torrent[-1], torrent[-2], torrent[1]
            if title not in self.torrents:
                self.torrents[title] = done
                continue

            if self.torrents[title] != '100%' and done == '100%':
                to_speak.append(title)
                self.torrents[title] = done

        if to_speak:
            tux.tts.speak('New torrents')
            for title in to_speak:
                tux.tts.speak('%s torrent done' % title)
                time.sleep(1)


class TransmissionPlugin(NestorPlugin):

    active = True
    sound = True
    action = TransmissionMonitor

    def __init__(self):
        self.torrents = dict()

    def ready(self, now):
        return True

    def setup_action(self, action):
        super(TransmissionPlugin, self).setup_action(action)
        action.torrents = self.torrents


def register(daemon):
    daemon.plugins.append(TransmissionPlugin())
