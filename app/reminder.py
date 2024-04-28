"""
Definition of class Reminder
"""
#!/usr/bin/env python3
# coding: utf-8
#t
# pressure_v0
#
# ===
# Todo:
#
# Notes
#
# ===
# M.Alexandre   apr.28  creation
#

# #############################################################################
#
# Import zone
#
from datetime import datetime
import nextcord


# #############################################################################
#
# Class
#

class Reminder:
    """
    Reminder class to store reminder contents
    """
    def __init__(self,
                 content:str,
                 time:datetime,
                 channel,
                 author:str,
                 author_pic:nextcord.Asset):
        self.content = content
        self.time=time
        self.channel = channel
        self.author=author
        self.author_pic=author_pic
