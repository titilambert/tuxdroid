# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import os
import re
import time
import email
from email.header import decode_header
from nestor import TuxAction, NestorPlugin


class MailChecker(TuxAction):

    def _decode_header(self, header):
        return ' '.join(unicode(t, 'latin1' if c is None else c)
                        for t, c in decode_header(header))

    def action(self, tux):
        to_clean, to_speak = True, []
        for mailbox_path in self.config['paths']:
            messages = [os.path.join(mailbox_path, 'new', fname) for fname
                        in os.listdir(os.path.join(mailbox_path, 'new'))]
            messages += [os.path.join(mailbox_path, 'cur', fname) for fname
                         in os.listdir(os.path.join(mailbox_path, 'cur'))
                         if 'S' not in fname.rsplit(':', 1)[1]]
            to_clean &= not bool(messages)

            for msg_path in messages:
                msg = email.message_from_file(open(msg_path))
                if msg['Message-Id'] in self.seen_email:
                    continue

                self.seen_email.add(msg['Message-Id'])
                subject = self._decode_header(msg['Subject'])
                author = re.split(" *<.*@.*\..{2,3}>",
                                  self._decode_header(msg['From']))[0]

                to_speak.append('%s de [%s]' % (subject, author))

        if to_speak:
            tux.tts.speak('Nouveaux emails')
            for m in to_speak:
                tux.tts.speak(m.encode("latin1"))
                time.sleep(1)

        if to_clean:
            # We don't want seen_email to grow too much
            self.seen_email.clear()


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
