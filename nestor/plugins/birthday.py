# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

from nestor import TuxAction


class Birthday(TuxAction):

    active = True
    sound = True
    name = u'Anniversaire'

    @classmethod
    def ready(cls, now):
        return ((now.day, now.month) in cls.config['data']
                and (now.hour % 3) == 0 and now.minute == 0)

    def action(self, tux):
        now = datetime.datetime.now()
        tux.flippers.on(3, finalState='DOWN', speed=5)

        tux.tts.speak("C'est l'anniversaire de :", 'Julie')
        for person in self.data[(now.day, now.month)]:
            tux.tts.speak(person.encode('latin1'), 'Julie')


def register(daemon):
    daemon.plugins.append(Birthday)
