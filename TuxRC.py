#!/usr/bin/python -i
## TuxRC v0.2!
##Copyright (C) 2009 Sean <admin@technologyisyourfriend.com>"
##This program is designed to control a remote (or local) tux droid.
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#=============CHANGELOG===================
##Format
##Version DD/MM/YYY Dev Name

##V0.2 6/1/2009 Sean
##                  First commit


#==========TODO===========
##closeEyes()
##openEyes()
##blink(n)
##flashEyes(n)
##munch(n)
##flap(n)
##spin180()
##spin360()
##spinr()
##spinl()
##getLight()

#sys module is required
import sys

#import tuxisalive.api
from tuxisalive.api import *

#extra modules in case the end user wants to play :)
import math
import threading
import thread
import os

#Display welcome message
print("Welcome to TuxRC v0.2!")
print ("Copyright (C) 2009 Sean <admin@technologyisyourfriend.com>")
print("This program is designed to control a remote (local) tux droid.")
print
print("For more details on the Tux Droid, visit http://www.kysoh.com") 
print
print("    This program is free software: you can redistribute it and/or modify")
print("    it under the terms of the GNU General Public License as published by")
print("    the Free Software Foundation, either version 3 of the License, or")
print("    (at your option) any later version.")
print
print("    This program is distributed in the hope that it will be useful,")
print("    but WITHOUT ANY WARRANTY; without even the implied warranty of")
print("    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
print("    GNU General Public License for more details.")
print
print("    You should have received a copy of the GNU General Public License")
print("    along with this program.  If not, see <http://www.gnu.org/licenses/>.")
print

#Ask user for address of server
def connect():
    #make tux global so that it can bbe used elsewhere in the script 
    global tux
    print("Note: Use http://www.whatsmyip.org/more for details on your internal and external addresses.")
    print
    print("Please be sure that port 720 is accessible on the remote host.")
    #print a blank line
    print 
#    try:
#        address = input("Please enter the address of the server (127.0.0.1 for the local Tux): ")
#        print
#    except:
#        print('Please enter the address in quotes. For example, "127.0.0.1" Please run this script again.')
#        print
#        #exit the python console 
#        quit()
    address = "127.0.0.1"
    #Connect to Tux Droid server

    #Define the tux object tux by using the address and port of the Tux Droid
    try:
        tux = TuxAPI(address, 270)

        #Gain access to tux
        tux.server.autoConnect(CLIENT_LEVEL_RESTRICTED, 'TuxGuestUser', 'TuxPass')
        #Alert the remote party
        tux.tts.speak("Alert! Someone has connected using Tux RC.")
    except:
        print("ERROR: Could not connect to the server! Please try again.")
        print
        #exit the python console 
        quit()
    
    #Define say()
def say(message):
#open the mouth
    try:
        tux.mouth.open()
        
    #Speak the message passed, use voice x and y % pitch
        tux.tts.speak(message,"Ryan", 120)
        
    #close the mouth...er...beak
        tux.mouth.close()
    except:
        print ("ERROR: TTS FAILED")
        tux.mouth.close()

#define finish
def finish():
#alert the parties

    say("The Tux RC user has disconnected")
    print("Control released.")

    #Release control of the server
    tux.access.release()

    #Disconnect from server 
    tux.server.disconnect()

    #Destroy the tux object (clean up)
    tux.destroy()
    
    #exit the python console 
    quit()

#desplay help documentation
def help():
    print("The fallowing methods are built into TuxRC:")
    print("     say(message)")
    print("         Opens the beak, says the massage, and closes the beak.")
    print('         Example: say("Hello world!")')
    print
    print("   help()")
    print("         Displays this message.")
    print('         Example: help()")')
    print
    print("     finish()")
    print("         Closes all connections the right way and ends this script.")
    print('         Example: finish()')
    print
    print("          DO NOT CLOSE THE TERMINAL WINDOW! USE finish()")
    print
    print("          You can also use all the things from tuxisalive.api.")
    print
    print("          Lastly, have fun!")
    #main
connect()

#Display welcome
print("Woo hoo! Everything is running smoothly.")
#dispplay help
help()
print
#let the user know to press enter
print ("PRESS ENTER TO ENTER THE PROMPT")
