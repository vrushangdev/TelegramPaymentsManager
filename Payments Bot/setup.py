#!./env/bin/python
# -*- coding: utf-8 -*-

import yaml
import logging
from telethon import TelegramClient, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = yaml.load(open('config.yml', 'r'))

api_id = config['api_id']
api_hash = config['api_hash']

client = TelegramClient("./default.session", api_id, api_hash).start()
