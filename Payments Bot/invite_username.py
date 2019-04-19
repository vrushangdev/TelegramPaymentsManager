#!./env/bin/python
# -*- coding: utf-8 -*-

import yaml
import csv
import logging
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import InputPeerUser
from time import sleep
from os import listdir
from os.path import isfile, join
import time
import datetime

#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = yaml.load(open('config.yml', 'r'))

api_id = config['api_id']
api_hash = config['api_hash']

client = TelegramClient("./default.session", api_id, api_hash).start()
group = client.get_entity(config['group_username'])

print("inviter accoutn has signed in")

def invite(username):
    from telethon.tl.functions.channels import InviteToChannelRequest

    try:
        u = client.get_entity(username)
        client(InviteToChannelRequest(
            group,
            [ u ]
            ))
    except Exception as e:
        print("  !! couldn't invite @{}: {}".format(username, str(e)))

