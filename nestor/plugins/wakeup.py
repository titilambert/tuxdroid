# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


try:
    import mpd
    HAS_MPD = True
except ImportError:
    HAS_MPD = False

import urllib

from nestor import TuxAction, NestorPlugin

class WakeUp(TuxAction):

    def action(self, tux):
        tux.eyes.open()
        tux.led.both.on()
	# Alarm 
	tux.flippers.on(3,tux.flippers.getPosition(),5)
	tux.tts.speak('Wake up Wake up Wake up Wake up Wake up')
	tux.flippers.on(3,tux.flippers.getPosition(),5)
	tux.eyes.on(3,'OPEN')
        # Enable idle_behavior
        urllib.urlopen("http://localhost:270/0/idle_behavior/start?")
	# end alarm
	# Enable sound for all plugins
        for plugin in self.plugins:
            if getattr(plugin, 'sound', False):
                plugin.active = True
	# MPD
        if HAS_MPD and self.config.get('stream', False):
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
    snooze = -1

    def __init__(self, plugins):
        super(WakeUpPlugin, self).__init__()
        self.plugins = plugins

    def ready(self, now):
	print self.snooze
	if now.minute == self.snooze :
	    self.snooze = (self.snooze + self.config['snooze']) % 60
	    return True
	elif (now.minute == self.config['minute'] and now.hour == self.config['hour']):
	    self.snooze = ( self.config['minute'] + self.config['snooze'] ) % 60
    	    return True
	else:
	    return False

    def setup_action(self, action):
        super(WakeUpPlugin, self).setup_action(action)
        action.plugins = self.plugins


def register(daemon):
    daemon.plugins.append(WakeUpPlugin(daemon.plugins))
