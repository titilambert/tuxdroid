# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import random
import datetime
from nestor import TuxAction, NestorPlugin


class TimeToSleep(TuxAction):

    def action(self, tux):
        # Shut down the leds they interfer with the light level sensor
        tux.led.both.off()

        light_level = float(tux.status.requestOne('light_level')[0])
        if light_level < 0.6:
            # Shutdown the audio plugins
            for plugin in self.plugins:
                if getattr(plugin, 'sound', False):
                    plugin.active = False

            tux.tts.speak('Au dodo', 'Bruno')
            tux.eyes.close()
        elif (self.launched_at.minute % self.config['reminder']) == 0:
            tux.eyes.onAsync(3, 'OPEN')
            tux.tts.speak('Il faudrait aller dormir', 'Bruno')


class TimeToSleepPlugin(NestorPlugin):

    action = TimeToSleep
    active = True
    sound = True

    def __init__(self, plugins):
        super(TimeToSleepPlugin, self).__init__()
        self.plugins = plugins

    def ready(self, now):
        return (self.config['start'] <= now.hour <= self.config['stop']) and \
                (now.minute % self.config['interval']) == 0

    def setup_action(self, action):
        super(TimeToSleepPlugin, self).setup_action(action)
        action.plugins = self.plugins


def register(daemon):
    daemon.plugins.append(TimeToSleepPlugin(daemon.plugins))
