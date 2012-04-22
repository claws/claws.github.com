---
layout: post
title: "Creating a Twisted friendly, pywws based, live weather service"
tags: 
- python
- twisted
- pywws
- zmq
- 0mq
meta-description: "A Python Twisted friendly, pywws based, live weather station" 
# Don't change the disqus identifier even if the url changes. It uniquely
# associates comments with the post.
disqus-identifier: "creating_a_twisted_friendly,_pywws_based,_live_weather_service"
---

<!-- excerpt start -->
When free time permits I try to improve the state of my home automation system.
Recently I have been working towards converting my monolithic Pachube feed updating 
software into a collection of ZMQ based services to improve the reliability of the system.

Most recently I have been trying to incorporate the pywws based wireless weather
station software into one of these services. Today I got it working and thought
I'd post about the pywws modifications.
<!-- excerpt end -->

The pywws software seems quite good. It looks like lots of people use it and
I found it quite easy to install and use. But to integrate it consistently with
my existing Twisted based software I needed to make it a bit more Twisted
friendly. 

This was not because the pywws tools lacks capability.  The pywws software is 
synchronous with lots of blocking <code>while</code> loops that do not fit well with 
the Twisted model that is the basis for many of my software tools.

These modifications are just for me but might be of use to someone, somewhere. 

The modifications started out by creating my own weather station object deriving from
a pywws.WeatherStation.weather_station object. I then proceeded to override blocking 
calls with non-blocking calls. 

As I was focused primarily on providing a live weather station service I made some 
additonal changes to support that easily. These may or may not already be provided
by pywws - at the time I couldn't find similar capabilities that I could just reuse.

The callback chains started getting a bit crazy so I then converted many of them
to make use of the <code>@defer.inlineCallbacks</code> decorator. This gives the code a more
synchronous look that on the surface seems easier to understand.

The Twist-ification changes affected the pywws.WeatherStation.weather_station and
the underlying USB device used to obtain data from the wireless weather station
head unit.

I'm sure it could be much improved. For example, the USB device could still block
the reactor doing memory reads, but the read count is kept low to minimise this.

I've posted the code in the following gist: [A Python Twisted friendly pywws Weather Station](https://gist.github.com/2464017) 

I have subsequently wrapped this into a ZMQ based service (using tx0mq) that publishes 
live weather station data to connected subscribers. I'll post about the ZMQ stuff later.



