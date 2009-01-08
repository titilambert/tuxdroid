# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


from nestor import TuxAction, NestorPlugin


class Horloge(TuxAction):

    def action(self, tux):
        tux.mouth.open()
        tux.tts.speak(self.launched_at.strftime('%H:%M'), 'Bruno')
        tux.mouth.close()


class HorlogePlugin(NestorPlugin):

    action = Horloge
    active = True
    sound = True

    def ready(self, now):
        return (now.minute % self.config['interval']) == 0

def register(daemon):
    daemon.plugins.append(HorlogePlugin())
