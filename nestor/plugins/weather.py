# -*- encoding: utf8 -*-
# This file is part of nestor. The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.


from nestor import TuxAction, NestorPlugin
import urllib
from xml.dom.minidom import parse, parseString

class Weather(TuxAction):

    def action(self, tux):
	# Get weather from internet
        # Get degrees 
	print self.config['city'].encode('utf8')
        if self.config['degree'] == "C":
                # Celsius
             	urlweather = urllib.urlopen('http://www.google.com/ig/api?weather=' + self.config['city'].encode('utf8'))
        else:
                # Fahrenheit
		urlweather = urllib.urlopen('http://www.google.com/ig/api?weather=' + self.config['city'])
	# Encoding conversion
	weather = unicode(urlweather.readline(), 'iso8859-15')
	weather = weather.encode('utf8')
	# Read weather xml
	dom = parseString (weather)
	# Get current information
	condition = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('condition')[0].getAttribute('data')
	if self.config['degree'] == "C":
	    temperature = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_c')[0].getAttribute('data') + unicode("° Celsius", 'iso8859-15')
	else:
	    temperature = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('temp_f')[0].getAttribute('data') + unicode("° Fahrenheit", 'iso8859-15')
	humidity = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('humidity')[0].getAttribute('data')
	wind = dom.getElementsByTagName('current_conditions')[0].getElementsByTagName('wind_condition')[0].getAttribute('data')
	# Let speak little tux ;)	
        tux.mouth.open()
	tux.tts.speak(	"The current weather, at " + self.config['city'].encode('latin-1') + 
			", is " + condition.encode('latin-1') +
			", with a temperature " + temperature.encode('latin-1')

)
        tux.mouth.close()


class WeatherPlugin(NestorPlugin):

    action = Weather
    active = True
    sound = True

    def ready(self, now):
        if self.config['interval'] < 0:
	    return now.minute == self.config['minute'] and now.hour == self.config['hour']
	elif self.config['minute'] > -1 and self.config['hour'] > -1:
	    if now.minute % self.config['interval'] == 0:
		return True
	    elif now.minute == self.config['minute'] and now.hour == self.config['hour']:
		return True
	    else:
		return False
	else:
	    return now.minute % self.config['interval']

def register(daemon):
    daemon.plugins.append(WeatherPlugin())
