# -*- coding: utf-8 -*-
"""
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.

@author: Thorin, Erèsue
"""

import random
import os
import threading
import time
import requests
import uuid



class bstats(threading.Thread):
    def __init__(self,plugin_id,is_micropython,logger):
        threading.Thread.__init__(self)
        self.id = plugin_id
        self.create_bstat_dictionary()
        self.is_micropython = is_micropython
        self.logger = logger
        
    def create_bstat_dictionary(self):
        systeminfo = os.uname()
        sysname = systeminfo[0]
        release = systeminfo[2]
        version = systeminfo[3]
        machine = systeminfo[4]
        
        self.logger.debug("sysname",sysname,"release",release,"version",version,"machine",machine)
        serverUUID = uuid.uuid1()
        self.bstat_dict = {
          "serverUUID": serverUUID.__str__(),
          "osName": sysname,
          "osArch": "Empty for now",
          "osVersion": version,
          "coreCount": machine,
          "plugins": [
            {
              "pluginName": "Phantom",
              "id": self.id,
              "pluginVersion": 0,
              "customCharts": [
                {
                  "chartId": "pings",
                  "data": [
                    {
                      "value": 6
                    }
                  ]
                },
                {
                  "chartId": "joins",
                  "data": [
                    {
                      "value": 3
                    }
                  ]
                },
                {
                  "chartId": "logging",
                  "data": [
                    {
                      "value": "all"
                    }
                  ]
                },
                {
                  "chartId": "mode",
                  "data": [
                    {
                      "value": "2"
                    }
                  ]
                }
              ]
            }
          ]
        }
    def send_data(self):
        
        url = 'https://bstats.org/submitData/server-implementation'
        res = requests.post(url, json=self.bstat_dict)
        self.logger.debug("Sent message to bstats")
        if res.text == "":
            pass #TODO idk, some errorprocessing
        
    
    def run(self):
        initial_delay = 60*3*(1+random.uniform(0, 1))#seconds
        second_delay = 60*30*(random.uniform(0, 1)) 
        loop_delay = 60*30
        
        time.sleep(initial_delay)
        self.send_data()
        
        time.sleep(second_delay+initial_delay)
        while True:
            self.send_data()
            time.sleep(loop_delay)