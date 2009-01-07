# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import datetime
from nestor import TuxAction

class TrainWarning(TuxAction):

    active = True
    sound = True
    name = u'Rappel train'

    @classmethod
    def ready(cls, now):
        m10_now = now + datetime.timedelta(minutes=cls.config['interval'])
        return [m10_now.hour, m10_now.minute] in cls.config['data']

    def action(self, tux):
        tux.tts.speak(u'Train à prendre dans 10 minutes'.encode('latin1'),
                      "Bruno")


def register(daemon):
    daemon.plugins.append(TrainWarning)
