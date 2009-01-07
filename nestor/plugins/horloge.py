# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import datetime
from nestor import TuxAction


class Horloge(TuxAction):

    active = True
    sound = True
    name = u'Horloge'

    @classmethod
    def ready(cls, now):
        return (now.minute % cls.config['interval']) == 0

    def action(self, tux):
        tux.mouth.open()
        now = datetime.datetime.now()
        tux.tts.speak(now.strftime('%H:%M'), 'Bruno')
        tux.mouth.close()


def register(daemon):
    daemon.plugins.append(Horloge)
