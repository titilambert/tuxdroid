# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import random
import datetime
from nestor import TuxAction, NestorPlugin
import urllib
import time

class TimeToSleep(TuxAction):

    sleep = False

    def action(self, tux):
        # Shut down the leds they interfer with the light level sensor
	tux.led.both.off()
	# Wait 1 second to not light the sensor
	time.sleep(1)

        light_level = float(tux.status.requestOne('light_level')[0])
        if light_level < 1:
            # Shutdown the audio plugins
            for plugin in self.plugins:
                if getattr(plugin, 'sound', False):
                    plugin.active = False
	
	    # Disable idle_behavior
 	    urllib.urlopen("http://localhost:270/0/idle_behavior/stop?")
	    # Good night
            tux.tts.speak('Good night')
            tux.eyes.close()
        #elif (self.launched_at.minute % self.config['reminder']) == 0:
        #    tux.eyes.onAsync(3, 'OPEN')
	#    tux.led.both.on()
        #    tux.tts.speak('You have to go to bed')
        else:
	    tux.mouth.open()
            tux.eyes.onAsync(3, 'OPEN')
	    while tux.led.both.getState() != "ON" :
		    tux.led.both.on()
            tux.tts.speak('You have to go to bed')
	    tux.flippers.on(3,tux.flippers.getPosition(),5)
            tux.mouth.close()


class TimeToSleepPlugin(NestorPlugin):

    action = TimeToSleep
    active = True
    sound = True

    def __init__(self, plugins):
        super(TimeToSleepPlugin, self).__init__()
        self.plugins = plugins

    def ready(self, now):
        return   (self.config['start'] <= now.hour <= self.config['stop']) and (now.minute % self.config['reminder']) == 0   

    def setup_action(self, action):
        super(TimeToSleepPlugin, self).setup_action(action)
        action.plugins = self.plugins


def register(daemon):
    daemon.plugins.append(TimeToSleepPlugin(daemon.plugins))
