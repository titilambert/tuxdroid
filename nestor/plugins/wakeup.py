# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import mpd
from nestor import TuxAction

class WakeUp(TuxAction):

    active = True
    name = u'Alarme'

    @classmethod
    def ready(cls, now):
        return (now.minute == cls.config['minute']
                and now.hour == cls.config['hour'])

    def action(self, tux):
        tux.eyes.open()
        tux.led.both.on()
        tux.tts.speak('Debout paillasse !', 'Bruno')

        for plugin in self.plugins:
            if getattr(plugin, 'sound', False):
                plugin.active = True

        client = mpd.MPDClient()
        client.connect('localhost', 6600)
        for d in client.outputs():
            if d['outputname'] != 'TuxDroid':
                client.disableoutput(int(d['outputid']))
            else:
                client.enableoutput(int(d['outputid']))
        client.clear()
        client.add(self.config['stream'])
        client.play()


def register(daemon):
    daemon.plugins.append(WakeUp)
    WakeUp.plugins = daemon.plugins
