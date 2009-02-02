# -*- coding: utf-8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


from nestor import TuxAction, NestorPlugin
import re
import dbus

class Kopete(TuxAction):

    def action(self, tux):
        # Connection 
        bus = dbus.SessionBus()
        dbusKopete = bus.get_object("org.kde.kopete", "/Kopete")
        # Get all contacts :
        contacts = dbusKopete.contacts()
        # Check if contacts are online or not
        for contactInfo in contacts :
            contact = contactInfo.split(":")[2]
            connected = dbusKopete.isContactOnline(contact)
            if connected :
                # Get contact properties
                contactProperties = dbusKopete.contactProperties(contact)
                # Check if contact leave a message
                if contactProperties["pending_messages"] != None :
                    # If yes then we remove html tags
                    kopeteMessage = re.sub('','',contactProperties["pending_messages"])
                    # Get contact Name
                    contactname = dbusKopete.getDisplayName(contact)
                    # Remove funking windows messenger tags ...
                    contactname = re.sub('\[[^!\]](?:[^\]]|\n)*\]', '' , contactname)
                    # We test the contact name lenght
                    if len(contactname) <= 10:
                        # If lenght of contactname is less than 10 then we use his name
                        contactSpeaking = contactname
                    else:
                        # else we use email address
                        contactSpeaking = contact
                    # Then tux speak
                    tux.mouth.open()
                    message = "You have a new message. %s says : %s " % (contactSpeaking,kopeteMessage)
                    tux.tts.speak(message)
                    tux.mouth.close()
      

class KopetePlugin(NestorPlugin):

    action = Kopete
    active = True
    sound = True

    def ready(self, now):
        if (now.minute % self.config['interval']) == 0:
            # Connection 
            bus = dbus.SessionBus()
            dbusKopete = bus.get_object("org.kde.kopete", "/Kopete")
            # Get all accounts
            accounts = dbusKopete.accounts()
            for account in accounts:
                accountinfo = dbusKopete.contactProperties(account)
                # If one account status is the same as config status ( default is "Away" )
                if accountinfo["status"] == self.config["status"]:
                    # Then return True
                    return True
            # If no account is the same as config status ( default is "Away" ) then return False
            return False
        else:
            return False
            

def register(daemon):
    daemon.plugins.append(KopetePlugin())
