# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import re
import time
import mailbox
from email.header import decode_header
from nestor import TuxAction


class MailChecker(TuxAction):

    active = True
    sound = True
    name = u'Vérification e-mail'

    @classmethod
    def ready(cls, now):
        return (now.minute % cls.config['interval']) == 0

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
                messages.append((author, subject))

        if messages:
            tux.tts.speak('Nouveaux emails', 'Bruno')
            for a, s in messages:
                tux.tts.speak(s.encode('latin1'))
                tux.tts.speak(("de %s" % a).encode("latin1"), 'Bruno')
                time.sleep(2)


def register(daemon):
    daemon.plugins.append(MailChecker)
