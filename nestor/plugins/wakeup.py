# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import mpd
from nestor import TuxAction, NestorPlugin

class WakeUp(TuxAction):

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


class WakeUpPlugin(NestorPlugin):

    action = WakeUp
    active = True

    def __init__(self, plugins):
        super(WakeUpPlugin, self).__init__()
        self.plugins = plugins

    def ready(self, now):
        return (now.minute == self.config['minute']
                and now.hour == self.config['hour'])

    def setup_action(self, action):
        super(WakeUpPlugin, self).setup_action(action)
        action.plugins = self.plugins


def register(daemon):
    daemon.plugins.append(WakeUpPlugin(daemon.plugins))
