# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.

import os
import re
import time
import email
from email.header import decode_header
from nestor import TuxAction, NestorPlugin


import imaplib
import poplib
# proto = imap | pop3
# port
# SSL = no | yes
# server = imap.gmail.com
# connect = imaplib.IMAP4_SSL(server, port) | imaplib.IMAP4(server, port) | imaplib.POP3(server, port) | imaplib.POP3_SSL(server, port)
# connect.login(user,passwd)
#
# Select mailbox
# mailbox = default=> INBOX | OTHER
# status , count = connect.select(mailbox,1)  # 1 read only mode
#
# Get last message
# status , data = connect.fetch( count[0] , '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
# data[0][1]
#
# Get unseen messages
# status , data = connect.search(None,'UNSEEN')
# unseen_messages = data[0].split()
#
# Get new messages
# status, data = toto.search(None, 'NEW')
# new_messages = data[0].split()
#
# unseen_messages + new_messages





class MailReader(TuxAction):

    def _decode_header(self, header):
        return ' '.join(unicode(t, 'latin1' if c is None else c)
                        for t, c in decode_header(header))

    def action(self, tux):
	if self.config['port'] :
	    port = self.config['port']
	elif self.config['protocol'] == 'imap' and self.config['SSL'] == False :	
	    port = 143
	elif self.config['protocol'] == 'imap' and self.config['SSL'] == True :	
	    port = 993
	elif self.config['protocol'] == 'pop3' and self.config['SSL'] == False :	
	    port = 25
	elif self.config['protocol'] == 'pop3' and self.config['SSL'] == True :	
	    port = 995
 	# Connection
        if self.config['protocol'] == 'imap' and self.config['SSL'] == True :
            connection = imaplib.IMAP4_SSL(self.config['server'], port)
        elif self.config['protocol'] == 'imap' and self.config['SSL'] == False :
            connection = imaplib.IMAP4(self.config['server'], port)
        elif self.config['protocol'] == 'pop3' and self.config['SSL'] == True :
            connection = imaplib.POP3_SSL(self.config['server'], port)
        elif self.config['protocol'] == 'pop3' and self.config['SSL'] == False :
            connection = imaplib.POP3(self.config['server'], port)
        else :
            print "CONFIG ERROR"
	# Login
	connection.login(str(self.config['user']),str(self.config['password']))
	# Select Mailbox
        if self.config['mailbox'] :
	    mailbox = self.config['mailbox']
        else :
	    mailbox = 'INBOX'
	status , count = connection.select(mailbox,1) 
	if count[0] > 0 :
	    # There is at least one new message
            # Get unseen messages
            status , data = connection.search(None,'UNSEEN')
 	    unseen_messages = data[0].split()
            # Get new messages
            status , data = connection.search(None,'NEW')
            new_messages = data[0].split()
            # Merge new messages
	    messages = new_messages + unseen_messages
	    temp = [] 
	    for message in messages :
                temp.append(int(message))
	    temp.sort()
	    messages = temp[:]
	    # Reading new messages
	    if len(messages) == 1 :
	        tux.tts.speak("You have a new message")
	    else :
		tux.tts.speak("You have " + len(messages) + " new messages")   
	else :
	    # No new message
	    tux.tts.speak("You don't have messages")
	# disconnection
	connection.close()
        connection.logout()
	


class MailReaderPlugin(NestorPlugin):

    active = True
    sound = True
    action = MailReader

    def __init__(self):
        self.seen_email = set()

    def ready(self, now):
        return (now.minute % self.config['interval']) == 0

    def setup_action(self, action):
        super(MailReaderPlugin, self).setup_action(action)


def register(daemon):
    daemon.plugins.append(MailReaderPlugin())
