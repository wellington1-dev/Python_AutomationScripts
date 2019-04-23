#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp
import subprocess
import time
import datetime

"""
    Example of reminder rules file :
    _ = [
        ({'min': range(0, 60, 5), 'sec': (0,)}, "Go home, you are drunk !"),
    ]
"""

PATH = os.getenv('REMINDER') or os.path.join(os.getenv("HOME"), "reminder")
IMG  = os.getenv('REMINDER_IMG') or\
       os.path.join(os.getenv("HOME"),"box/nuke.png")

def _check_cron(timetuple, cron):
    return (not cron.get('year') or timetuple[0] in cron.get('year')) and\
           (not cron.get('mon') or timetuple[1] in cron.get('mon')) and\
           (not cron.get('mday') or timetuple[2] in cron.get('mday')) and\
           (not cron.get('hour') or timetuple[3] in cron.get('hour')) and\
           (not cron.get('min') or timetuple[4] in cron.get('min')) and\
           (not cron.get('sec') or timetuple[5] in cron.get('sec')) and\
           (not cron.get('wday') or timetuple[6] in cron.get('wday')) and\
           (not cron.get('yday') or timetuple[7] in cron.get('yday'))


def notif(title="Reminder", body="Body !!!", timeout=3000):
    cmd = ("dbus-send",
           "--type=method_call",
           "--dest=org.freedesktop.Notifications",
           "/org/freedesktop/Notifications",
           "org.freedesktop.Notifications.Notify",
           "string:reminder", # app
           "uint32:0", # replace old notif
           "string:{}".format(IMG), # icon
           "string:{}".format(title), # title
           "string:{}".format(body), # body
           "array:string:''", # action
           "dict:string:string:'',''", # hints
           "uint32:{}".format(timeout), # timeout
    )

    subprocess.check_output(cmd)


def main():
    while True:
        r = imp.load_source('reminder', PATH)
        timetuple = datetime.datetime.now().timetuple()
        for i in r._:
            if _check_cron(timetuple, i[0]):
                notif(body=i[1], timeout=-1)
        time.sleep(1)


if __name__ == "__main__":
    main()
