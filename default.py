# -*- coding: utf-8 -*-

import os
import time
import json

from src import InstaBot
from src.check_status import check_status
from src.feed_scanner import feed_scanner
from src.follow_protocol import follow_protocol
from src.unfollow_protocol import unfollow_protocol

if os.path.isfile('./config.hsn'):
	
	print('Starting....')
	
	configFile = open('./config.hsn','r')
	configFile = json.loads(configFile.read())
	
	bot = InstaBot(
		login=configFile['username'],
		password=configFile['password'],
		database_name=configFile['username'],
		like_per_day=1000,
		tag_list=configFile['hashtag'].split(','),
		tag_blacklist=configFile['antihashtag'].split(','),
		log_mod=1
	)

	#while True:
	bot.new_auto_mod()
else:
	print('Not Install')