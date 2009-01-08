# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


import random
import datetime
from nestor import TuxAction, NestorPlugin


class TimeToSleep(TuxAction):

    def action(self, tux):
        now = datetime.datetime.now()
        tux.eyes.open()
        tux.led.both.off()
        led = random.choice([tux.led.left, tux.led.right])
        led.on()
        if 0 <= now.hour < 2:
            tux.tts.speak(u'Je suis vraiment fatigué'.encode('latin1'),
                          'Bruno')
        elif 2 <= now.hour < 4:
            tux.tts.speak(u'Ça va être difficile demain'.encode('latin1'), 
                          'Bruno')
        else:
            tux.tts.speak(u"Il est vraiment l'heure de dormir".encode('latin1'),
                          'Bruno')
        led.off()
        tux.eyes.close()


class TimeToSleepPlugin(NestorPlugin):

    action = TimeToSleep
    active = True
    sound = True

    def ready(self, now):
        return True
        return (0 <= now.hour <= 6) and ((now.minute % 30) == 0)


def register(daemon):
    daemon.plugins.append(TimeToSleepPlugin())
