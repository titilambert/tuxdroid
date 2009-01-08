# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import time

from nestor import TuxAction, NestorPlugin


class Birthday(TuxAction):

    def action(self, tux):
        tux.flippers.on(3, finalState='DOWN', speed=5)

        celebrate = []
        to_celebrate = self.data[(self.launched_at.day, self.launched_at.month)]

        for person in to_celebrate:
            if person not in self.celebrated:
                self.celebrated.add(person)
                celebrate.append(person)

        if celebrate:
            tux.tts.speak(u'Anniversaire de '.encode('latin1', 'Julie'))
            for person in celebrate:
                tux.tts.speak(person.encode('latin1'), 'Julie')
                time.sleep(2)


class BirthdayPlugin(NestorPlugin):

    action = Birthday
    active = True
    sound = True

    def __init__(self):
        self.celebrated = set()

    def ready(self, now):
        return ((now.day, now.month) in self.config['data']
                and (now.hour % 3) == 0 and now.minute == 0)

    def setup_action(self, action):
        super(BirthdayPlugin, self).setup_action(action)
        action.data = self.config['data']
        action.celebrated = self.celebrated


def register(daemon):
    daemon.plugins.append(BirthdayPlugin())
