# -*- coding: utf-8 -*-

import os
import json
from instabot_py import InstaBot

if os.path.isfile('./config.hsn'):
	
	print('Starting....')
	
	configFile = open('./config.hsn','r')
	configFile = json.loads(configFile.read())
	
	bot = InstaBot(
		login=configFile['username'],
		password=configFile['password'],
		database_name="database",
		session_file="session.session",
		like_per_day=1000,
		tag_list=configFile['hashtag'].split(','),
		tag_blacklist=configFile['antihashtag'].split(','),
		log_mod=1
	)

	#while True:
	bot.new_auto_mod()
else:
	print('Not Install')