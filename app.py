#  -*- coding: utf-8 -*-

from flask import Flask,render_template
from flask import request
from flask import abort
import urllib
import requests
import re
import os
import json
import signal
import subprocess
import platform
import psutil

global subrun,pid,r,sig,logfile

r = False
pid = None

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse
#from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/', methods=['GET','POST'])
def index():
	
	configFile = open('./config.hsn','r')
	configFile = json.loads(configFile.read())

	if configFile['install'] == "false":
		welcome = {
			'text' : 'Please.. install',
			'status' : 'notinstall'
		}
	else:
		
		if os.path.isfile('./errors.log'):
			logread = open('errors.log', 'r')
			logread = logread.read()
		else:
			logread = 'null'
			
		welcome = {
			'text' : 'Good.. Script Installed',
			'status' : 'installed',
			'terminal' : logread
		}

	return render_template("welcome.html",welcome=welcome)
	
@app.route('/run', methods=['GET','POST'])
def run():
	global subrun,pid,r,sig,logfile
	
	if os.path.isfile('./errors.log'):
		logread = open('errors.log', 'r').read()
	else:
		logread = 'null'
	
	if r==False:
		subrun = subprocess.Popen('python default.py', shell=True, stdout=open('logfile', 'a'))
		pid = subrun.pid
		r = True
		
		statusText = {
			'text' : 'Running....',
			'status' : 'running',
			'terminal': logread
		}
		
	else:
		pid = None
		statusText = {
			'text' : 'Already Running....',
			'status' : 'running',
			'terminal':	 logread
		}
	
	return render_template("status.html",statusText=statusText)
	
@app.route('/stop', methods=['GET','POST'])
def stop():
	global subrun,pid,r,sig

	open('errors.log', 'w').write('')
	
	if os.path.isfile('./errors.log'):
		logread = open('errors.log', 'r').read()
	else:
		logread = 'null'
	
	if r == True:
		if platform.system() == 'Windows':
			subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pid))
		else:
			process = psutil.Process(pid)
			for proc in process.children(recursive=True):
				proc.kill()
			process.kill()
		r = False
		pid = None
		
		statusText = {
			'text' : 'Stop...',
			'status' : 'stop',
			'terminal': logread
		}
		
	else:
		statusText = {
			'text' : 'Already Stop...',
			'status' : 'stop',
			'terminal': logread
		}
	
	return render_template("status.html",statusText=statusText)
	
@app.route('/install', methods=['GET','POST'])
def install():
	
	install = {
		'text' : 'Install',
		'status' : 'nonInstall'
	}
	
	return render_template("install.html",install=install)
	
@app.route('/installed', methods=['GET','POST'])
def installed():
	
	istatus = 'success'
	if request.method == 'POST':
		try:
			
			username = request.form['username']
			password = request.form['password']
			hashtag = request.form['hashtag']
			antihashtag = request.form['antihashtag']
			license = request.form['license']
			
			#r = requests.get('https://api.hayatikodla.net/instabot/')
			#if r.status_code == 200:
			#r = r.json()
			#if r['status'] == 'success':
			
			configFile = open('./config.hsn','w')
			configFile.write('{ "install" : "true","username":"'+username+'","password":"'+password+'","hashtag":"'+hashtag+'","antihashtag":"'+antihashtag+'"}')
		
			itext = 'License Validate'
			#else:
				#itext = 'License not approved'
				#istatus = 'danger'
			#else:
				#itext = 'License not approved'
				#istatus = 'danger'
		except EOFError:
			itext = 'Empty Values'
			istatus = 'danger'
	else:
		itext = 'Install Page'

	installed = {
		'text' : itext,
		'status' : istatus
	}
	
	return render_template("install.html",install=installed)

@app.route('/ver', methods=['GET','POST'])
def ver():
	return "1.0.14"

if __name__ == "__main__":
	app.run()