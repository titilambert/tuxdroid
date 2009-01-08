# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import re
import time
import mailbox
from email.header import decode_header
from nestor import TuxAction, NestorPlugin


class MailChecker(TuxAction):

    def _decode_header(self, header):
        return ' '.join(unicode(t, 'ascii' if c is None else c)
                        for t, c in decode_header(header))

    def action(self, tux):
        mb = mailbox.Maildir(self.config['path'],
                             factory=mailbox.MaildirMessage)

        messages = []
        for k in mb.iterkeys():
            m = mb.get_message(k)
            if m.get_subdir() == 'new':
                subject = self._decode_header(m['Subject'])
                author = re.split("<.*@.*\..{2,3}>",
                                  self._decode_header(m['From']))[0]
                message_id = m['Message-Id']
                messages.append((author, subject, message_id))

        to_speak = []
        for a, s, id in messages:
            if id not in self.seen_email:
                self.seen_email.add(id)
                to_speak.append('%s de %s' % (s, a))

        if to_speak:
            tux.tts.speak('Nouveaux emails', 'Bruno')
            for m in to_speak:
                tux.tts.speak(m.encode("latin1"), 'Bruno')
                time.sleep(2)


class MailCheckPlugin(NestorPlugin):

    active = True
    sound = True
    action = MailChecker

    def __init__(self):
        self.seen_email = set()

    def ready(self, now):
        return (now.minute % self.config['interval']) == 0

    def setup_action(self, action):
        super(MailCheckPlugin, self).setup_action(action)
        action.seen_email = self.seen_email


def register(daemon):
    daemon.plugins.append(MailCheckPlugin())
