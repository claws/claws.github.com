---
layout: post
title: "Publication of Australian weather observations using MQTT"
tags:
 - MQTT
 - Twisted
meta-description:
# Don't change the disqus identifier even if the url changes. It uniquely
# associates comments with the post.
disqus-identifier: "publication_of_australian_weather_observations_using_mqtt"
summary: How MQTT can be used to publish Australian weather observation data
---


## Introduction

The Australian Bureau of Meteorology (BoM) makes plenty of data available to users (Eg. forecasts via FTP & HTTP, observations via HTTP in JSON, to name a few), but parsing this information in a generic way is often difficult because of inconsistencies in the data from state to state and time of day. I've found forecast information the most inconsistent while the JSON observations are generally pretty good.

The standard BoM web services requires a user or application to actively request a resource from the BoM. Ideally, I'd like to simply subscribe for location specific weather information and receive an update whenever the BoM publishes new data for that location.
<!-- excerpt start -->
This post covers how the Australian Bureau of Meteorology could publish weather observation data in a small, efficient format to many receivers. Publishing data in this manner would make it very simple for mobile applications and automated systems to efficiently obtain BoM data.
<!-- excerpt end -->

## Background

I retrieve data from the BoM for use with my home automation system. I built [txbom](https://github.com/claws/txBOM), a Python Twisted library, to help me do this. I use the BoM forecast and current observation data, combined with calendar events, to construct a specifically formatted text file that is pushed through text-to-speech, saved as MP3 and finally played as the first track in my morning alarm play-list.

My home automation system has similarities to architectures I use as work. Consequently it is almost exclusively built on a [ZMQ](www.zeromq.org) architecture with automatic application and service discovery. However I recently bought some Arduinos and a Raspberry Pi to play around with and to extend my home automation system. As the majority of my home automation system is built on ZMQ I naturally began looking for ZMQ libraries for Arduino and Raspberry Pi. Not finding a good candidate for the Arduino I widened my search and came across [MQTT](www.mqtt.org).

From the MQTT site:

    MQTT stands for MQ Telemetry Transport. It is a publish/subscribe, extremely simple and lightweight messaging protocol, designed for constrained devices and low-bandwidth, high-latency or unreliable networks. The design principles are to minimise network bandwidth and device resource requirements whilst also attempting to ensure reliability and some degree of assurance of delivery. These principles also turn out to make the protocol ideal of the emerging “machine-to-machine” (M2M) or “Internet of Things” world of connected devices, and for mobile applications where bandwidth and battery power are at a premium.
    [MQTT FAQ](http://mqtt.org/faq)

This technology looked promising. I set up a Mosquitto MQTT broker on the Raspberry Pi which was surprisingly easy. I use [twisted](http://twistedmatrix.com/trac/) as the framework for most of my projects so I grabbed [MQTT-For-Twisted-Python](https://github.com/adamvr/MQTT-For-Twisted-Python) and built a simple publisher and subscriber to try it out.

From that quick test it seemed to me that MQTT could provide a very simple way to connect constrained Arduino style devices and standard compute nodes into my automation architecture. However, I'm not totally convinced. I quite like the decentralised features of my ZMQ based system whereas MQTT requires a broker which can be a single point of failure. However, good enough is often good enough so I decided to give it a try by converting a few of my applications over to use MQTT to how it goes.

I first converted my current cost application which was relatively simple. I actually found the hardest part of the whole conversion was coming up with a good topic naming convention. I wanted the topics to be fairly intuitive. I've since come across a few blog posts on the same topic. Potentially that is a good sign, the technology is easy and works - the hard part is designing your topic structure.

Next up for conversion was an application that I use to retrieve BoM forecasts and observations. Again this was relatively straight-forward. It was while I was converting this application that I got to thinking _wouldn't it be great if the BoM offered MQTT as one of their standard web services_? I, along with countless others, could get rid of our custom parsers and simply subscribe to a BoM MQTT broker to automatically receive BoM updates.

How hard could it be? To test this concept, I created an application that would periodically retrieve the current observations for all weather stations from the BoM, convert them into some useful format and then publish them to a MQTT broker. I found a BoM web [resource](http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDY03021.txt) that conveniently had observations for every Australian state and territory so I used that as the data source.

As a simple demonstration, the application seemed to work fine so I thought I'd share it as may be of use to someone. I like how simple it was to install the broker and get a simple example up and running. I'll be using MQTT to publish BoM weather data information to my local MQTT broker.

### Publisher

The publisher application starts by downloading the current observations from a standard HTTP request. Then the pre-formatted text observation data is extracted. The data is examined to determine when it was updated - the observation data is updated hourly by the BoM. The application schedules another retrieval to occur a few minutes after the next update time - to give them BoM some time to update the files on their web site. After scheduling the next retrieval it begins parsing the data by breaking it into state chunks and then further into data fields for individual weather stations. The data is converted into JSON format and looks like this:

{% highlight javascript %}
{"rain_mm": "N/A", "updated": "Mon Apr 29 10:10:24 UTC 2013", "temperature": "18", "copyright": "Copyright Commonwealth of Australia , Bureau of Meteorology (ABN 92 637 533 532)", "cloud_cover": "N/A", "pressure_hpa": "1023.7", "wind_direction": "ENE", "rel_humidity": "65", "hour": "0830", "precis": "Fine", "source": "http://www.bom.gov.au/", "temperature_max": "N/A", "longitude": "13862", "visibility_km": "N/A", "latitude": "3492", "wind_speed_kmh": "2.70", "temperature_min": "N/A", "day": "29"}
{% endhighlight %}

I added a copyright and a source field in an attempt to comply with the BoM's rules on secondary [redistribution](http://reg.bom.gov.au/other/copyright.shtml).

The topics published by this application follow the topic pattern __bomau__/__&lt;state&gt;__/__&lt;station&gt;__. An example of the topic layout, showing only the state of South Australia expanded, can be seen in this following picture:

<center>
<img src="/resources/topics.png">
</center>


To be kind to the `test.mosquitto.org` public test broker I restricted the application to only publish information for one station; Adelaide, South Australia. To publish BoM observation data for all states and stations one would simply remove the lines that constrain it to only publish data for Adelaide, South Australia.

### Subscriber

To test the publisher a subscriber application was created. It connects to the `test.mosquitto.org` broker and subscribes for updates on the topic `bomau/South Australia/Adelaide`.

## The Code

<script src="https://gist.github.com/claws/5482174.js"></script>

When the scripts are run:

From the publisher:

{% highlight bash %}
$ ./bomau_publisher.py
2013-04-30 00:22:24,356: INFO - bomau_publisher.py:179 - BoM Observation Client starting
2013-04-30 00:22:24,356: INFO - bomau_publisher.py:186 - Creating MQTT client
2013-04-30 00:22:24,707: INFO - bomau_publisher.py:126 - Connected to MQTT Broker
2013-04-30 00:22:25,053: DEBUG - bomau_publisher.py:271 - Requesting new observation data from: http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDY03021.txt
2013-04-30 00:22:25,053: INFO - log.py:532 - Starting factory <HTTPClientFactory: http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDY03021.txt>
2013-04-30 00:22:25,589: DEBUG - bomau_publisher.py:277 - Retrieved new observation data
2013-04-30 00:22:25,596: INFO - bomau_publisher.py:315 - Next observation retrieval will occur after delay of: 0:22:58.404152
detected 8 state sections
2013-04-30 00:22:25,596: DEBUG - bomau_publisher.py:439 - Ignoring Adelong - no data available
2013-04-30 00:22:25,596: DEBUG - bomau_publisher.py:439 - Ignoring Albury - no data available
2013-04-30 00:22:25,596: DEBUG - bomau_publisher.py:439 - Ignoring Alstonvill - no data available
...
2013-04-30 00:22:25,639: DEBUG - bomau_publisher.py:439 - Ignoring Windy Hbor - no data available
2013-04-30 00:22:25,639: DEBUG - bomau_publisher.py:439 - Ignoring WndringCom - no data available
2013-04-30 00:22:25,640: DEBUG - bomau_publisher.py:439 - Ignoring WongnH Res - no data available
2013-04-30 00:22:25,640: DEBUG - bomau_publisher.py:441 - West Australia contained 126 stations
2013-04-30 00:22:25,640: DEBUG - bomau_publisher.py:441 - Antarctica contained 4 stations
2013-04-30 00:22:25,640: INFO - bomau_publisher.py:218 - BoM observations for 8 regions retrieved successfully
2013-04-30 00:22:25,641: INFO - bomau_publisher.py:243 - South Australia has 72 stations
2013-04-30 00:22:25,642: INFO - bomau_publisher.py:254 - Beginning to publish 1 updates to MQTT Broker
2013-04-30 00:22:25,642: INFO - bomau_publisher.py:465 - Completed publishing observation updates.
2013-04-30 00:22:25,642: INFO - log.py:532 - Stopping factory <HTTPClientFactory: http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDY03021.txt>
2013-04-30 00:23:25,086: INFO - bomau_publisher.py:135 - Ping received from MQTT broker
{% endhighlight %}

From the subscriber:

{% highlight bash %}
$ ./bomau_subscriber.py
2013-04-30 00:22:18,009: INFO - bomau_subscriber.py:59 - Creating MQTT client
2013-04-30 00:22:18,386: INFO - bomau_subscriber.py:23 - Connected to MQTT Broker
2013-04-30 00:22:18,736: INFO - bomau_subscriber.py:35 - Subscribed for topic: bomau/South Australia/Adelaide
2013-04-30 00:22:26,024: INFO - bomau_subscriber.py:41 - Update received. Topic: bomau/South Australia/Adelaide, Message: {"rain_mm": "0.0/12", "updated": "Mon Apr 29 14:10:24 UTC 2013", "temperature": "15", "copyright": "Copyright Commonwealth of Australia , Bureau of Meteorology (ABN 92 637 533 532)", "cloud_cover": "N/A", "pressure_hpa": "1025.6", "wind_direction": "ENE", "rel_humidity": "70", "hour": "1130", "precis": "Fine", "source": "http://www.bom.gov.au/", "temperature_max": "N/A", "longitude": "13862", "visibility_km": "N/A", "latitude": "3492", "wind_speed_kmh": "2.16", "temperature_min": "N/A", "day": "29"}
2013-04-30 00:23:18,732: INFO - bomau_subscriber.py:28 - Ping response received from MQTT broker
{% endhighlight %}



## Conclusion

Providing BoM data through a MQTT channel seems like a good way of distributing BoM data efficiently to insterested parties. It would provide a useful resource for people building automated devices and systems that can perform actions based on weather data. It might also be a good opportunity to apply consistency to BoM data such as forecasts.



