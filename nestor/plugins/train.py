# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import datetime
from nestor import TuxAction, NestorPlugin

class TrainWarning(TuxAction):

    def action(self, tux):
        text = u'Train à prendre dans %s minutes' % self.config['interval']
        tux.tts.speak(text.encode('latin1'), "Bruno")


class TrainWarningPlugin(NestorPlugin):

    action = TrainWarning
    active = True
    sound = True

    def ready(self, now):
        m10_now = now + datetime.timedelta(minutes=self.config['interval'])
        return [m10_now.hour, m10_now.minute] in self.config['data']


def register(daemon):
    daemon.plugins.append(TrainWarningPlugin())
