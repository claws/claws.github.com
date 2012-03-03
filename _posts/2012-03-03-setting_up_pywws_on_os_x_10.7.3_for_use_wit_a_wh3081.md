---
layout: post
title: "Setting up pywws on OS X 10.7.3 for use with a WH3081"
tags: 
- python
- home automation
meta-description: "Instructions for getting a WH3081 wireless weather station working on OS X 10.7.3 with pywws" 
---

<!-- excerpt start -->
This post details how I installed and configured software dependecies that will eventually allow me to upload data, received from my WH3081 wireless weather station, to my [feed](https://pachube.com/feeds/42745) at Pachube. It is mostly just so I remember how I did it but also because using OS X with the weather station is not the typical use case for pywws.
<!-- excerpt end -->

To use pywws on OS X requires the use of hidapi to communicate with the USB device. This means that cython-hidapi and hence Cython are required dependencies that must be install prior to going anywhere near pywws.

Download [Cython](http://cython.org/) and install.

    {% highlight bash %}
    tar zxf Cython-0.15.1.tar.gz
    cd Cython-0.15.1
    sudo python setup.py install
    {% endhighlight %}

Download [cython-hidapi](https://github.com/gbishop/cython-hidapi) and install. I downloaded the zip file using the zip button in Github.

    {% highlight bash %}
    unzip gbishop-cython-hidapi-d65adfc.zip
    cd gbishop-cython-hidapi-d65adfc
    python setup-mac.py build
    sudo python setup.py install
    {% endhighlight %}

Edit the <code>try.py</code> script to add your weather station USB vendor id and product id. I just had to comment out the default value and uncomment the line with the typical weather station values. I also commented out the section that attempts to write data to the device - it is just random data and I didn't want that getting written to the device. 

So the script ended up looking like this:

    {% highlight python %}
    import hid
    import time
    
    for d in hid.enumerate(0, 0):
        keys = d.keys()
        keys.sort()
        for key in keys:
            print "%s : %s" % (key, d[key])
        print ""

    try:
        print "Opening device"
        #h = hid.device(0x461, 0x20)
        h = hid.device(0x1941, 0x8021) # Fine Offset USB Weather Station
    
        print "Manufacturer: %s" % h.get_manufacturer_string()
        print "Product: %s" % h.get_product_string()
        print "Serial No: %s" % h.get_serial_number_string()
    
        # try non-blocking mode by uncommenting the next line
        #h.set_nonblocking(1)
    
        # try writing some data to the device
        #for k in range(10):
        #    for i in [0, 1]:
        #        for j in [0, 1]:
        #            h.write([0x80, i, j])
        #            d = h.read(5)
        #            if d:
        #                print d
        #            time.sleep(0.05)
    
        print "Closing device"
        h.close()
    
    except IOError, ex:
        print ex
        print "You probably don't have the hard coded test hid. Update the hid.device line"
        print "in this script with one from the enumeration list output above and try again."
    
    print "Done"
    {% endhighlight %}

Run the modified <code>try.py</code> script. It does not really do much. If it worked properly it should not report an error.


Download [pywws](http://code.google.com/p/pywws/) and test that the weather station software can communicate with the weather station USB device. 

NOTE: The readme file in pywws indicates the need to install hidapi and cython-hidapi but I found this was not necessary. The cython-hidapi installation includes the underlying hidapi c module as well as the python wrapper.

    {% highlight bash %}
    tar zxf pywws-12.02_r487.tar.gz
    cd pywws-12.02_r487
    python TestWeatherStation.py -vv -d -h 5
    09:26:13:pywws.WeatherStation.CUSBDrive:using pywws.device_cython_hidapi
    09:26:13:pywws.weather_station:type change 1080 -> 3080
    {'data_changed': 0, 'timezone': 8, 'unknown_18': 0, 'unknown_19': 0, 'data_count': 1464, 'min': {'hum_out': {'date': '2012-02-14 15:25', 'val': 11}, 'windchill': {'date': '2012-02-08 03:14', 'val': 11.200000000000001}, 'dewpoint': {'date': '2012-02-14 15:25', 'val': 1.7000000000000002}, 'temp_in': {'date': '2011-01-31 20:31', 'val': 19.1}, 'abs_pressure': {'date': '2012-02-05 00:35', 'val': 989.2}, 'rel_pressure': {'date': '2012-02-05 00:35', 'val': 993.4000000000001}, 'hum_in': {'date': '2012-02-24 07:25', 'val': 33}, 'temp_out': {'date': '2012-02-08 03:14', 'val': 11.200000000000001}}, 'abs_pressure': 1003.1, 'alarm_1': {'hum_out_hi': False, 'hum_in_lo': False, 'hum_in_hi': False, 'hum_out_lo': False, 'time': False, 'bit3': False, 'wind_dir': False, 'bit0': False}, 'alarm_3': {'temp_out_hi': False, 'wind_chill_lo': False, 'dew_point_lo': False, 'temp_in_lo': False, 'wind_chill_hi': False, 'temp_in_hi': False, 'temp_out_lo': False, 'dew_point_hi': False}, 'alarm_2': {'wind_ave': False, 'wind_gust': False, 'rain_hour': False, 'pressure_rel_lo': False, 'pressure_abs_hi': False, 'rain_day': False, 'pressure_rel_hi': False, 'pressure_abs_lo': False}, 'max': {'hum_out': {'date': '2012-02-05 08:23', 'val': 99}, 'windchill': {'date': '2012-02-25 15:42', 'val': 42.900000000000006}, 'dewpoint': {'date': '2012-02-27 14:23', 'val': 20.700000000000003}, 'uv': {'val': 14}, 'wind_ave': {'date': '2012-02-05 11:36', 'val': 6.800000000000001}, 'rain': {'week': {'date': '2012-02-19 00:00', 'val': 7.199999999999999}, 'total': {'date': '2012-03-02 14:22', 'val': 118.8}, 'day': {'date': '2012-03-03 00:00', 'val': 56.699999999999996}, 'hour': {'date': '2012-03-02 15:00', 'val': 56.699999999999996}, 'month': {'date': '2010-01-01 12:00', 'val': 0}}, 'temp_in': {'date': '2012-02-25 14:41', 'val': 31.900000000000002}, 'illuminance': {'val': 173263.7}, 'abs_pressure': {'date': '2012-02-12 09:40', 'val': 1015.2}, 'rel_pressure': {'date': '2012-02-12 09:40', 'val': 1019.6}, 'hum_in': {'date': '2011-01-31 21:06', 'val': 64}, 'temp_out': {'date': '2012-02-25 15:42', 'val': 42.900000000000006}, 'wind_gust': {'date': '2012-02-05 17:06', 'val': 10.5}}, 'settings_1': {'pressure_inHg': False, 'pressure_hPa': True, 'temp_out_F': False, 'pressure_mmHg': False, 'rain_in': False, 'temp_in_F': False, 'bit4': False, 'bit3': False}, 'settings_2': {'wind_bft': False, 'wind_mps': False, 'wind_knot': False, 'bit7': False, 'bit6': False, 'bit5': False, 'wind_kmph': True, 'wind_mph': False}, 'unknown_07': 0, 'unknown_06': 0, 'unknown_05': 0, 'unknown_04': 0, 'unknown_03': 0, 'rel_pressure': 1007.5, 'unknown_01': 127, 'unknown_09': 0, 'unknown_08': 0, 'date_time': '2012-03-03 09:31', 'current_pos': 29516, 'display_2': {'temp_out_temp': True, 'rain_hour': False, 'rain_month': False, 'rain_week': False, 'temp_out_chill': False, 'rain_day': True, 'temp_out_dew': False, 'rain_total': False}, 'display_3': {'illuminance_fc': False, 'bit7': False, 'bit6': False, 'bit5': False, 'bit4': True, 'bit3': True, 'bit2': False, 'bit1': False}, 'alarm': {'hum_out': {'lo': 45, 'hi': 70}, 'windchill': {'lo': 0, 'hi': 20.0}, 'dewpoint': {'lo': -10.0, 'hi': 10.0}, 'uv': 10, 'wind_ave': {'ms': 18.0, 'bft': 0}, 'rain': {'day': 150.0, 'hour': 3.0}, 'temp_in': {'lo': 0, 'hi': 20.0}, 'illuminance': 299973.60000000003, 'abs_pressure': {'lo': 960.0, 'hi': 1040.0}, 'rel_pressure': {'lo': 960.0, 'hi': 1040.0}, 'hum_in': {'lo': 35, 'hi': 65}, 'temp_out': {'lo': -10.0, 'hi': 30.0}, 'time': '12:00', 'wind_dir': 0, 'wind_gust': {'ms': 10.4, 'bft': 0}}, 'display_1': {'wind_gust': False, 'show_day_name': False, 'show_year': False, 'time_scale_24': False, 'pressure_rel': False, 'alarm_time': True, 'date_mdy': False, 'clock_12hr': False}, 'read_period': 30}
    min -> temp_out -> {'date': '2012-02-08 03:14', 'val': 11.200000000000001}
    alarm -> hum_out -> {'lo': 45, 'hi': 70}
    rel_pressure -> 1007.5
    abs_pressure -> 1003.1
    Recent history
    2012-03-03 09:31:00 {'status': 64, 'hum_out': None, 'wind_gust': None, 'uv': None, 'wind_ave': None, 'rain': 18.9, 'temp_in': 23.0, 'illuminance': None, 'abs_pressure': 1003.1, 'delay': 12, 'hum_in': 61, 'temp_out': None, 'wind_dir': 132}
    2012-03-03 09:19:00 {'status': 64, 'hum_out': None, 'wind_gust': None, 'uv': None, 'wind_ave': None, 'rain': 18.9, 'temp_in': 23.1, 'illuminance': None, 'abs_pressure': 1003.0, 'delay': 30, 'hum_in': 60, 'temp_out': None, 'wind_dir': 132}
    2012-03-03 08:49:00 {'status': 0, 'hum_out': 88, 'wind_gust': 0.7000000000000001, 'uv': 4, 'wind_ave': 0.30000000000000004, 'rain': 18.9, 'temp_in': 23.5, 'illuminance': 25572.100000000002, 'abs_pressure': 1003.3000000000001, 'delay': 30, 'hum_in': 58, 'temp_out': 18.900000000000002, 'wind_dir': 2}
    2012-03-03 08:19:00 {'status': 0, 'hum_out': 99, 'wind_gust': 0, 'uv': 1, 'wind_ave': 0, 'rain': 18.9, 'temp_in': 23.0, 'illuminance': 5608.3, 'abs_pressure': 1003.0, 'delay': 30, 'hum_in': 59, 'temp_out': 15.100000000000001, 'wind_dir': 8}
    2012-03-03 07:49:00 {'status': 0, 'hum_out': 99, 'wind_gust': 0, 'uv': 0, 'wind_ave': 0, 'rain': 18.9, 'temp_in': 22.6, 'illuminance': 1952.8000000000002, 'abs_pressure': 1002.7, 'delay': 30, 'hum_in': 61, 'temp_out': 14.100000000000001, 'wind_dir': 14}
{% endhighlight %}

I ran the pywws package from the current directory without installing it. The pywws package can be installed using:
    {% highlight bash %}
    sudo python setup.py install
    {% endhighlight %}

These instructions were also followed on my MacMini where this software will eventually run (that machine is on 24/7 doing various automation tasks, etc). The only real difference being that the python commands were explcitly run with python2.7 on the MacMini running OS X 10.6.8, where python 2.7 is not the default python.
