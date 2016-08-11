__author__ = 'rui'
#coding=utf-8

import urllib2
import json
import math
import time


def rad(d):
    return d * math.pi / 180.0


def distanceLatLng(lat1, lng1, lat2, lng2):
    radlat1 = rad(lat1)
    radlat2 = rad(lat2)
    a = radlat1 - radlat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radlat1) * math.cos(radlat2) * math.pow(math.sin(b / 2), 2)))
    earth_radius = 6378.137
    s = s * earth_radius
    return math.fabs(s)


def getCityLoc(city):
    city = urllib2.quote(city)
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + city + "&sensor=false"
    print(url)
    headers = {'Content-Type': 'application/json'}
    data = None
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    data = json.load(response)
    response.close()
    location = data['results'][0]['geometry']['location']
    print location
    return location


def distance(city1, city2):
    loc1 = getCityLoc(city1)
    time.sleep(3)
    loc2 = getCityLoc(city2)
    return distanceLatLng(loc1['lat'], loc1['lng'], loc2['lat'], loc2['lng'])


if __name__ == "__main__":
    city1 = raw_input(">城市1：")
    city2 = raw_input(">城市2：")
    print("距离：{0}".format(distance(city1, city2)))