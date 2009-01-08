#!/usr/bin/python2.5
# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

__metaclass__ = type

import os
import sys
import re
import time
import signal
import datetime
import threading

import yaml

from tuxisalive.api import *


class Daemon(threading.Thread):

    plugins = []

    def __init__(self, config_path):
        super(Daemon, self).__init__()
        self.daemon = True
        self.config = config_path

        self.menu = Menu(self)
        self.reloader = ConfReloader(config_path, self)
        self.scheduler = Scheduler(config_path)

        self.stop = threading.Event()
        self.reload = threading.Event()

    def run(self):
        self.menu.start()
        self.reloader.start()

        self.prepare_scheduler()
        self.scheduler.start()

        while not self.stop.isSet():
            self.reload.wait(1)
            if self.reload.isSet():
                print 'Reloading config files'
                self.scheduler.cancel()

                self.scheduler = Scheduler(self.config)
                self.prepare_scheduler()
                self.scheduler.start()

                self.reload.clear()

    def prepare_scheduler(self):
        for plugin in self.plugins:
            self.scheduler.add_plugin(plugin)

    def _handle_TERM(self, signum=None, frame=None):
        self.scheduler.cancel()
        self.reloader.cancel()
        self.menu.stop.set()
        self.menu.join()
        self.stop.set()


class PerpetualTimer(threading._Timer):

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.isSet():
                return
            self.function(*self.args, **self.kwargs)


class ConfReloader(PerpetualTimer):

    def __init__(self, config_path, daemon):
        super(ConfReloader, self).__init__(10, self.check_config)
        self.path = config_path
        self.oldtime = None
        self.parent = daemon

    def check_config(self):
        if self.oldtime is None:
            self.oldtime = os.stat(self.path).st_mtime
            return

        mtime = os.stat(self.path).st_mtime
        if mtime > self.oldtime:
            self.oldtime = mtime
            self.parent.reload.set()


class Menu(threading.Thread):

    def __init__(self, daemon):
        super(Menu, self).__init__()
        self.stop = threading.Event()

        self.plugins = daemon.plugins
        self.tux = self.setup_tux()
        self.menu_idx = [0]

        self.menu = [(u'Son', [(u'Activer', self.sound),
                               (u'Désactiver', self.nosound)]),
                     (u'Lumières', [(u'Activer', self.wakeup),
                                    (u'Désactiver', self.dodo)]),
                     (u"Donner l'heure", self.whattime),
                     ]

    def setup_tux(self):
        tux = TuxAPI('127.0.0.1', 270)
        tux.server.autoConnect(CLIENT_LEVEL_FREE, 'Menu', 'NONE')

        if tux.access.waitAcquire(30, ACCESS_PRIORITY_NORMAL):
            tux.button.head.registerEventOnPressed(self.on_head)
            tux.button.left.registerEventOnPressed(self.on_left)
            tux.button.right.registerEventOnPressed(self.on_right)
            for name, value in globals().iteritems():
                if name.startswith('K_'):
                    tux.button.remote.registerEventOnPressed(self.on_remote,
                                                             value)
        tux.access.release()

        return tux

    def run(self):
        while not self.stop.isSet():
            time.sleep(1)
        self.tux.server.disconnect()
        self.tux.destroy()

    def on_head(self, *args):
        print args

    def on_left(self, *args):
        print args

    def on_right(self, *args):
        print args

    def on_remote(self, key, delta_t):
        action = {K_UP: lambda x: x-1,
                  K_DOWN: lambda x: x+1}

        if delta_t > 15:
            self.menu_idx = [0]
            current_menu = self.menu
        else:
            last_menu = self.menu_idx.pop()
            current_menu = self.menu
            for idx in self.menu_idx:
                current_menu = current_menu[idx][1]

            new_menu = action.get(key, lambda x:x)(last_menu) \
                    % len(current_menu)
            self.menu_idx.append(new_menu)

        current_item = current_menu[self.menu_idx[-1]]

        if key == K_OK and isinstance(current_item[1], (list, tuple)):
            self.menu_idx.append(-1)
        elif key == K_OK and callable(current_item[1]):
            t = threading.Thread(target=current_item[1])
            t.start()
        elif key in (K_UP, K_DOWN):
            t = threading.Thread(target=self.say, args=(current_item[0],))
            t.start()
        elif key == K_LEFT:
            if len(self.menu_idx) == 1:
                return
            self.menu_idx.pop()
            t = threading.Thread(target=self.say, args=(u'OK',))
            t.start()

    def say(self, message):
        self.tux.tts.speak(message.encode('latin1'), 'Bruno')

    def dodo(self):
        self.tux.led.both.off()
        self.tux.eyes.close()

    def wakeup(self):
        self.tux.eyes.open()
        self.tux.led.both.on()

    def whattime(self):
        now = datetime.datetime.now()
        self.tux.tts.speak(now.strftime('%H:%M'), 'Bruno')

    def nosound(self):
        for plugin in self.plugins:
            if getattr(plugin, 'sound', False):
                plugin.active = False
        self.say(u'OK')

    def sound(self):
        for plugin in self.plugins:
            if getattr(plugin, 'sound', False):
                plugin.active = True
        self.say(u'OK')


class Scheduler(PerpetualTimer):

    def __init__(self, config_path):
        super(Scheduler, self).__init__(60, self.launch_plugin)
        self.plugins = []
        self.config = yaml.load(open(config_path, 'r'))

    def add_plugin(self, plugin):
        plugin.config = self.config.get(plugin.__name__, {})
        self.plugins.append(plugin)

    def launch_plugin(self):
        now = datetime.datetime.now()
        for plugin in self.plugins:
            if plugin.active and plugin.ready(now):
                plugin.start(now)


class TuxAction(threading.Thread):

    def __init__(self, now):
        super(TuxAction, self).__init__(name=self.__class__.__name__)
        self.launched_at = now

    def run(self):
        tux = TuxAPI('127.0.0.1', 270)
        tux.server.autoConnect(CLIENT_LEVEL_RESTRICTED,
                               self.__class__.__name__, 'NONE')
        if tux.access.waitAcquire(30, ACCESS_PRIORITY_NORMAL):
            self.action(tux)
        tux.access.release()
        tux.server.disconnect()
        tux.destroy()


class NestorPlugin:

    action = TuxAction
    active = False

    def ready(self, now):
        return False

    def start(self, now):
        action = self.action(now)
        self.setup_action(action)
        action.start()

    def setup_action(self, action):
        action.config = self.config


def register_plugins(d):
    plugin_path = os.path.join(os.path.dirname(__file__), 'plugins')
    plugin_files = [fname[:-3] for fname in os.listdir(plugin_path)
                    if fname.endswith('.py')]
    if plugin_path not in sys.path:
        sys.path.append(plugin_path)

    for mod in [__import__(pf) for pf in plugin_files]:
        mod.register(d)


def main(conf_path):

    sys.stdout.flush()
    sys.stderr.flush()

    # Double fork daemonization
    pid = os.fork()
    if pid > 0:
        os._exit(0)

    os.setsid()

    pid = os.fork()
    if pid > 0:
        os._exit(0)

    d = Daemon(conf_path)
    register_plugins(d)

    open('nestor.pid', 'w').write(str(os.getpid()))
    signal.signal(signal.SIGTERM, d._handle_TERM)
    d.start()

    while not d.stop.isSet():
        time.sleep(1)
        sys.stdout.flush()
        sys.stderr.flush()

    d.join()
    os.remove('nestor.pid')

if __name__ == '__main__':
    main('nestor.conf')
