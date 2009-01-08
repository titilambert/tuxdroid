# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


from nestor import TuxAction, NestorPlugin

class TrainWarning(TuxAction):

    def action(self, tux):
        text = u'Train à prendre dans %s minutes' % self.config['interval']
        tux.tts.speak(text.encode('latin1'), "Bruno")


class TrainWarningPlugin(NestorPlugin):

    action = TrainWarning
    active = True
    sound = True

    @classmethod
    def ready(cls, now):
        m10_now = now + datetime.timedelta(minutes=cls.config['interval'])
        return [m10_now.hour, m10_now.minute] in cls.config['data']



def register(daemon):
    daemon.plugins.append(TrainWarningPlugin())
